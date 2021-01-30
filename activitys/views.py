import json
import os
import time
import base64
import pickle
import random
from urllib import parse
from urllib.parse import quote

import html2text
from django.shortcuts import render
from django_redis import get_redis_connection
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from tools import chang_imgname
from activitys.models import UserInfo, AdminArticle
from tools.util import upload_img_save
from users.models import UserRegist
from tools.response_code import code
from tools.logging_checked import login_check
from dwebsocket.decorators import accept_websocket
from django.conf import settings
from haystack.forms import ModelSearchForm
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from activitys.models import Activity, InterestTag
from django.views.generic.base import View


class Active(View):
    def get(self, request):
        return render(request, 'index.html')
    
    @login_check
    def post(self, request):
        '''
        用户创建活动 先验证登录 及权限
        再验证提交是否非空
        再查询当前标签的活动类型是否过多
        查询标签记录
        获取imageurl,没有就给默认图片
        插入数据库 成功后发布活动数+1
        最后创建活动返回200
        在django-redis中缓存activity中创建key=活动ID的集合 值为发起人act.user
        :param request:
        :return:
        '''
        res = json.loads(request.body)
        if not res:
            print('没有数据')
            return JsonResponse(code[10000])
        try:
            tag = res.get('kind')
            title = res.get('title')
            starttime = res.get('starttime')
            endtime = res.get('endtime', None)
            address = res.get('addr')
            condition = int(res.get('condition'))
            content = res.get('content')
        except Exception as e:
            print(e, '参数缺失')
            return JsonResponse(code[10000])
        try:
            interest = InterestTag.objects.get(interests=tag)
        except Exception as e:
            print(e, '活动标签查询异常')
            return JsonResponse(code[10002])
        user = request.myuser
        img_path = interest.img_url.name
        try:
            act = Activity.objects.create(user=user, tag=interest, subject=title, content=content,
                                          status=1, act_img=img_path, end_time=endtime, beg_time=starttime,
                                          condition=condition, activ_address=address)
        except Exception as e:
            print(e, '插入数据库异常')
            return JsonResponse(code[10001])
        
        # 修改活动图片
        img_data = res.get('img_data')
        user_str_id = str(act.id)
        if img_data:
            file_data = base64.b64decode(img_data.split(',')[1])
            filename = user_str_id + settings.IMG_END
            img_path = settings.DBACTIMG + filename
            save_res = upload_img_save(file_data, img_path)
            if save_res['code'] == 10501:
                print(save_res['message'])
            else:
                img_sql_path = settings.DBACTIMG + user_str_id + settings.IMG_END
                act.act_img = img_sql_path
                act.save()
        try:
            newact = get_redis_connection('newact')
            newact.delete('new_act' + act.tag.interests)
            newact.delete('new_act')
            user_list = [act.user.email]
            user_lists = json.dumps(user_list)
            activity = get_redis_connection('activitys')
            try:
                activity.hset(act.id, act.created_time.strftime('%Y-%m-%d'), user_lists)
                activity.expire(act.id, 60 * 60 * 24)
            except Exception as e:
                print('redis写入失败', e)
                act.delete()
                return JsonResponse(code[10005])
            # 每创建一个活动，全局活动数量 +1，便于websockte获取最新活动
            settings.ACTIVITY_NUM += 1
            # 当前用户发起活动的数量增加一个
            userinfos = UserInfo.objects.get(id=user.userinfo.id)
            userinfos.sponsor_num = userinfos.sponsor_num + 1
            userinfos.save()
            result = {'code': 200, 'actid': act.id}
        except Exception as e:
            print(e)
            act.delete()
            return JsonResponse(code[201])
        return JsonResponse(result)


# 存取结果
def get_result(page, label):
    lab = parse.unquote(label)
    if label:
        # 根据传入的标签，查询对应的兴趣对象，最终根据兴趣id，去除活动表中的，创建相关兴趣的活动
        labelobj = InterestTag.objects.filter(interests=lab)
        if labelobj:
            activity = Activity.objects.filter(status=1, tag=labelobj[0]).order_by('-created_time')[:80]
        else:
            return code[10006]
    else:
        # 如果没有label，表示是主页，不带tag，的页面刷新，所以：按创建时间倒叙取出活动
        activity = Activity.objects.filter(status=1).order_by('-created_time')
    if not activity:
        return code[201]
    # paginator 分页器对象， 第一个参数，对象列表，第二个此参数，每页显示的条数
    paginator = Paginator(activity, 8)
    
    # TODO 把 pagintor 存放在redis中 保存1天
    redisname = 'new_act' + lab
    newact = get_redis_connection('newact')
    newact.set(redisname, pickle.dumps(paginator), ex=60 * 60 * 24)
    # 数据格式化，后返回结果
    return make_result(paginator, page)

# 构造response并发送
def make_result(paginator, page):
    # 页总数
    numpages = paginator.num_pages
    # 获取当前页的对象列表
    act_list = paginator.page(page)
    # 当前页的对象列表中个数
    now_page = act_list.number
    data = []
    for act in act_list:
        content = act.content
        title = act.subject
        imgname = chang_imgname.parse_imgname(act.act_img.name)
        data.append({
            'id': act.id,
            'title': title,
            'content': content,
            'date': act.created_time.strftime('%Y-%m-%d'),
            'actimg': imgname,
            'label': act.tag.interests
        })
    result = {'code': 200, 'data': data, 'page': [now_page, numpages]}
    return result


@accept_websocket
def get_new(request, page):
    """
    获取主页跟标签页的最新活动信息 优先读取djredis
    按时间排序 筛选最近发布的活动
    把前80 名 放进django-redis
    按每8条数据分页， 把对应page的内容返回
    :return:
    """
    if request.method == 'GET':
        label = request.GET.get('tag', '')
        act_now_num = 0
        if request.is_websocket():
            # redis_activ = 'new_act' + label
            # newact = get_redis_connection('newact')
            # print(newact)
            # TODO 此处优化redis中拿去数据 ，要跟mysql中同步，
            # if newact.exists(redis_activ):
            #     paginator = pickle.loads(newact.get(redis_activ))
            #     result = make_result(paginator, page)
            # else:
            result = get_result(page, label)
            if not result:
                result = code[10007]
            request.websocket.send(json.dumps(result))

            while True:
                # 检查是否有新消息
                if settings.ACTIVITY_NUM > act_now_num:
                    settings.ACTIVITY_NUM -= 1
                    result = get_result(page, label)
                    print(']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
                    print(result)
                    request.websocket.send(json.dumps(result))
                time.sleep(1)
        return JsonResponse(code[10506])


def hyistorical_activities(request, page):
    """
    获取历史活动
    # 按点击量，收藏排行(pass)
    按创建时间排序
    把前80 名 放进django-redis
    按每8条数据分页
    把对应page的内容返回
    :param request:
    :return:
    """
    if request.method == 'GET':
        label = request.GET.get('tag', '')
        if label:
            lab = parse.unquote(label)
            labelobj = InterestTag.objects.filter(interests=lab)
            activity = Activity.objects.filter(status=3, tag=labelobj[0]).order_by('-created_time')[:80]
        else:
            activity = Activity.objects.filter(status=3).order_by('-created_time')[:80]
        if not activity:
            return JsonResponse(code[10007])
        paginator = Paginator(activity, 8)
        # TODO 把pagintor存放在redis中
        act_list = paginator.page(page)
        numpages = paginator.num_pages
        now_page = act_list.number
        data = []
        for act in act_list:
            content = act.content
            title = act.subject
            data.append({
                'id': act.id,
                'title': title,
                'content': content,
                'date': act.created_time.strftime('%Y-%m-%d'),
                'actimg': act.act_img.name,
                'label': act.tag.interests
            })
        result = {'code': 200, 'data': data, 'page': [now_page, numpages]}
        return JsonResponse(result)


class ActHotIndex(View):
    def get(self, request):
        pass

    def post(self, request):
        """
        首页最热活动展示
        最热： 点击量 收藏 综合排名前三
        先读django-redis  没有再查数据库
        保存数据 过期时间
        """
        # 0. 获取所有品类
        try:
            all_list = Activity.objects.all().order_by('-click_nums')[:3]
        except Exception as e:
            return JsonResponse[code[10507]]
        # 1. 首页最新活动默认显示三个
        index_data = []
        for item in all_list:
            index = {}
            index['act_id'] = str(item.id)
            index['subject'] = item.subject
            imgname = chang_imgname.parse_imgname(item.act_img.name)
            index['imgurl'] = imgname
            index_data.append(index)
        code[200]['data'] = index_data
        return JsonResponse(code[200])


# 直接从MySQL中获取数据
def active_users(request):
    """
        活动达人数据从后端集orderBy(发起活动数前60+参与活动数前60)，将这些用户形成集合，随机从中取8人在前端渲染展示
        从数据库获取发起活动数和参与活动数
        注意：在用户信息表里创建了发起活动和参与活动字段
            1.需要用户在创建活动时+1，删除活动时-1
            2.用户参与活动时+1
    """
    # 从数据库获取发起活动数前60名
    users1 = UserInfo.objects.order_by('-sponsor_num')
    # print('users1:', len(users1))
    if len(users1) > 60:
        set_users1 = set(users1[:10])
    else:
        set_users1 = set(users1)
    # print('set_users1:', len(set_users1))
    # 从数据库获取参与活动前60名
    users2 = UserInfo.objects.order_by('-participate_num')
    # print('users2:', len(users2))
    if len(users2) > 60:
        set_users2 = set(users2[:10])
    else:
        set_users2 = set(users2)
    set_active_users = set_users1 | set_users2  # miao!

    # 从集合中随机取8个用户
    if len(set_active_users) >= 8:
        active_users = random.sample(set_active_users, 8)
    else:
        active_users = set_active_users
    # print(len(active_users))
    # 将用户信息整理成列表
    data = []
    for _user in active_users:
        user_info = {}
        user_info['user_id'] = str(_user.user.id)
        user_info['nickname'] = _user.nickname
        user_info['gender'] = _user.gender
        user_info['hd_pic'] = str(_user.portrait)
        user_info['sign_words'] = _user.introduction
        user_info['sponsor_num'] = _user.sponsor_num
        user_info['participate_num'] = _user.participate_num
        user_info['tags'] = []
        # 取用户兴趣标签
        j = 0
        for tag in _user.interest.all():
            user_info['tags'].append(tag.interests)
            j += 1
            if j == 3:
                break
        data.append(user_info)
    code[200]['data'] = data
    return JsonResponse(code[200])



# 优先从redis中获取数据，redis中没有数据则从MySQL获取数据
def get_active_users(request):
    """
    用Django-redis实现
        活动达人数据从后端集orderBy(发起活动数前60+参与活动数前60)，将这些用户形成集合，随机从中取8人在前端渲染展示
        从数据库获取发起活动数和参与活动数
        注意：在用户信息表里创建了发起活动和参与活动字段
            1.需要用户在创建活动时+1，删除活动时-1
            2.用户参与活动时+1
    """
    # 127.0.0.1:8000/v1/user/actvuser2

    # 从数据库获取发起活动数前60名
    users1 = UserInfo.objects.order_by('-sponsor_num')
    if len(users1) > 10:
        set_users1 = set(users1[:10])
    else:
        set_users1 = set(users1)
    # 从数据库获取参与活动前60名
    users2 = UserInfo.objects.order_by('-participate_num')
    if len(users2) > 10:
        set_users2 = set(users2[:10])
    else:
        set_users2 = set(users2)
    set_active_users = set_users1 | set_users2

    users_data = []
    # 从redis中获取所有数据
    redis_conn = get_redis_connection('users')
    redis_index = redis_conn.get('active_users')

    # 判断内存中有无数据
    if redis_index is None:

        for _user in set_active_users:
            user_info = {}
            user_info['user_id'] = _user.user.id
            user_info['nickname'] = _user.nickname
            user_info['gender'] = _user.gender
            user_info['hd_pic'] = str(_user.portrait)
            user_info['sign_words'] = _user.introduction
            user_info['sponsor_num'] = _user.sponsor_num
            user_info['participate_num'] = _user.participate_num
            user_info['tags'] = []
            # 取用户兴趣标签
            j = 0
            for tag in _user.interest.all():
                user_info['tags'].append(tag.interests)
                j += 1
                if j == 3:
                    break
            users_data.append(user_info)
            # 写入缓存
        # 可考虑如缓存时压缩json串 zlib
        redis_conn.set("active_users", json.dumps(users_data), ex=30)
    else:
        users_data = json.loads(redis_index)
    if len(users_data) >= 8:
        data = random.sample(users_data, 8)
    else:
        data = users_data
    code[200]['data'] = data
    return JsonResponse(code[200])


# 优先从redis中获取数据，redis中没有数据则从MySQL获取数据
def get_admin_articles(request):
    """
    用Django-redis实现
        从官方文件中获取最新4篇文章，展示在主页窗口的第一屏
    """
    # 127.0.0.1:8000/v1/activitys/article
    # 从数据库获取管理员发布的最新四篇文章
    try:
        admin_user = UserRegist.objects.get(id=5)
        obj_articles = AdminArticle.objects.filter(user=admin_user).order_by('updated_time')[:4]
        print(obj_articles)
        print('obj_article:', len(obj_articles))
    except Exception as e:
        code[10009]['message'] = e
        return JsonResponse(code[10009])

    # 将数据封装在列表中
    article_data = []
    # 从redis中获取所有数据
    redis_conn = get_redis_connection('users')
    redis_index = redis_conn.get('admin_articles')
    # 判断内存中有无数据
    if redis_index is None:
        print("未使用缓存")
        for article in obj_articles:
            article_info = {}
            article_info['article_id'] = article.id
            article_info['user_id'] = article.user.id
            article_info['subject'] = article.subject
            article_info['content'] = article.content
            article_info['act_img'] = str(article.act_img)
            article_info['click_nums'] = article.click_nums
            article_info['created_time'] = str(article.created_time.date())
            article_info['updated_time'] = str(article.updated_time.date())
            article_data.append(article_info)
            # 写入缓存
        # 可考虑如缓存时压缩json串 zlib
        redis_conn.set("admin_articles", json.dumps(article_data), ex=30)
    else:
        print("使用缓存")
        article_data = json.loads(redis_index)
    code[200]['data'] = article_data
    return JsonResponse(code[200])


def article_info(request):
    article_id = request.GET.get('article_id')
    if not article_id:
        return JsonResponse(code[10003])
    try:
        article = AdminArticle.objects.get(id=article_id)
    except Exception as e:
        code[10003]['message'] = f'文章不存在:原因为{e}'
        return JsonResponse(code[10003])

    # 从redis中获取所有数据
    redis_conn = get_redis_connection('users')
    redis_index = redis_conn.get('article_info:%s' % article_id)
    article_info = {}
    # 判断内存中有无数据
    if redis_index is None:
        print("未使用缓存")
        article_info['article_id'] = article.id
        article_info['user_id'] = article.user.id
        article_info['subject'] = article.subject
        article_info['updated_time'] = str(article.updated_time.date())
        article_info['click_nums'] = article.click_nums
        article_info['act_img'] = str(article.act_img)
        article_info['content'] = [p.strip() for p in article.content.split('\n')]
        article_info['created_time'] = str(article.created_time.date())
        # 写入缓存
        # 可考虑如缓存时压缩json串 zlib
        redis_conn.set('article_info:%s' % article_id, json.dumps(article_info), ex=30)
    else:
        print("使用缓存")
        article_info = json.loads(redis_index)
    result = {'code': 200, 'data': article_info}
    return JsonResponse(result)


class ActivityDetailView(View):
    def get(self, request):
        pass

    def post(self, request):
        """
        活动详情信息获取
        """
        # 获取act_id
        data = request.body
        data = json.loads(data)
        print('进来了')
        act_id = int(data.get('act_id'))
        if act_id is None:
            return JsonResponse(code[10003])
        try:
            act = Activity.objects.get(id=act_id)
            act.click_nums  = act.click_nums + 1
            act.save()
        except Exception as e:
            print('进来', e)
            code[10003]['message'] = e
            return JsonResponse(code[10003])
        result = {"code": 200, 'subject': act.subject, 'content': act.content,
                  'starttime': act.beg_time.strftime('%Y-%m-%d'),
                  'like': act.likes}
        return JsonResponse(result)



def activitySearchView(request, page_now):
        """
        首⻚，table页查询功能
        1、通过前端传入的tag是否为空，决定是主页还是table搜索
        1、 通过ModelSearchForm判断查询字符串是否有效
        2、通过SearchQuerySet()获取文档信息
        3、如果没有获取到，主页请求则查询所有文档，并且返回，table页请求，则返回所有tag相关文档
        
        TODO 待添加各种搜索，  根据 活动标题关键字，点击量最高排序，活动id等
        """
        # 127.0.0.1:8000/active/search/1
        try:
            search_key = request.POST.get('q')
            tag_key = request.POST.get('tag')
            print('进来了哇')
            print(search_key, tag_key, '[[[[[[[[')
            if not search_key:
                return JsonResponse(code[10010])
            # 如果传入的tag有值， 表明是从table页发过来的请求；获取对应tag中的所有带有关键字的活动
            if tag_key:
                # table页搜索
                form_obj = ModelSearchForm(request.POST, load_all=True)
                tag_obj = InterestTag.objects.filter(interests=tag_key)[0]
                # 根据标签名查询标签id
                if form_obj.is_valid():
                    tag = "id:{} nickname:{}".format(str(tag_obj.id), tag_key)
                    first_sqs = SearchQuerySet().filter(content=tag)
                    sqs = first_sqs.filter(content=search_key).highlight(pre_tags=['<strong>'], post_tags=['</strong>'])
                    print(f'从tabl总共查询出了{len(sqs)}条数据')
                    if not len(sqs):
                        results = return_all_activ(tag, page_now)
                        return JsonResponse(results)
                    res_data_list = parse_sqs_data(sqs)
                else:
                    return JsonResponse(code[10011])
    
            # 主页搜索
            else:
                tag = None
                form_obj = ModelSearchForm(request.POST, load_all=True)
                if form_obj.is_valid():
                    query = form_obj.cleaned_data['q']
                    sqs = SearchQuerySet().filter(content=AutoQuery(query)).highlight(pre_tags=['<strong>'], post_tags=['</strong>'])
                    if not len(sqs):
                        results = return_all_activ(tag, page_now)
                        print(results)
                        return JsonResponse(results)
                else:
                    return JsonResponse(code[10011])
                print(f'当前从主页中查询出了{len(sqs)}条数据')
                res_data_list = parse_sqs_data(sqs)
                if not res_data_list:
                    return JsonResponse(return_all_activ(tag, page_now))
            all_page = return_page_num(sqs)
            result = {"code": 200, "data": res_data_list, 'page': [int(page_now), all_page]}
            print(result)
            return JsonResponse(result)
        except Exception as e:
            print(e)


def return_page_num(sqs):
    try:
        paginator_obj = Paginator(sqs, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        # 获取页码总数
        allpage = paginator_obj.num_pages
    except Exception as e:
        code[10012]['message'] = e
        return JsonResponse(code[10012])
    return allpage
    

def return_all_activ(tag, page_now):
    """返回所有tabl页 或者 主页的活动信息"""
    if tag:
        all_sqs = SearchQuerySet().filter(content=tag)
    else:
        all_sqs = SearchQuerySet().all()
    res_data_list = parse_sqs_all_type(all_sqs)
    all_page = return_page_num(all_sqs)
    result = {"code": 10015, 'info': '没有匹配到信息，展示所有信息', "data": res_data_list, 'page': [int(page_now), all_page]}
    return result


def parse_sqs_data(sqs):
    """
    根据content、text类型查询的数据解析函数
    """
    res_search_list = []
    for search_result_obj in sqs:
        res_search_dic = {}
        highlight_res_list = search_result_obj.highlighted
        parse_data = highlight_res_list[0].split('\n')
        if len(parse_data) != 5:
            continue
        res_search_dic["act_id"] = parse_data[0]
        res_search_dic["tag"] = parse_data[1].split(':')[2]
        res_search_dic["subject"] = parse_data[2]
        res_search_dic["content"] = parse_data[3]
        activ_model = Activity.objects.filter(id=res_search_dic["act_id"])[0]
        res_search_dic["imgurl"] = activ_model.act_img.name
        res_search_dic['date'] = activ_model.created_time.strftime('%Y-%m-%d')
        res_search_list.append(res_search_dic)
    return res_search_list

def parse_sqs_all_type(sqs):
    """ 根据字段类型查询的数据解析函数"""
    res_search_list = []
    for search_result_obj in sqs:
        res_search_dic = {}
        print(search_result_obj.id.split('.')[2])
        res_search_dic["act_id"] = search_result_obj.id.split('.')[2]
        res_search_dic["tag"] = search_result_obj.tag.split(':')[2]
        res_search_dic["subject"] = search_result_obj.subject
        res_search_dic["content"] = search_result_obj.content
        try:
            activ_model = Activity.objects.filter(id=res_search_dic["act_id"])[0]
        except Exception as e:
            print(e, ']]]]]]]]]]]]]]]]]')
            return JsonResponse(code[10013])
        res_search_dic["imgurl"] = activ_model.act_img.name
        res_search_dic['date'] = activ_model.created_time.strftime('%Y-%m-%d')
        res_search_list.append(res_search_dic)
        print(res_search_dic)
    return res_search_list


def pdf_md_transform(request):
        try:
            print('进来了')
            font_path = os.path.abspath('') + '/config/black.ttf'
            pdfmetrics.registerFont(TTFont("song", font_path))
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename={}.pdf'.format('nihao')
            p = canvas.Canvas(response)
            # flag = 8
            # print(len(note_obj.content))
            # if len(note_obj.content) > 1000:
            #     flag = -1
            # if 1000 > len((note_obj.content)) > 400:
            #     flag = 7
            # print(flag)
            p.translate(0.5 * inch, 10 * inch)
            # 设置字体
            p.setFont('song', 8)
            styleSheet = getSampleStyleSheet()
            style = styleSheet['Normal']
            style.fontName = 'song'
            style.fontSize = 12
            # 设置行距
            style.leading = 20
            # 首行缩进
            style.firstLineIndent = 32
            # 设置自动换行
            style.wordWrap = 'CJK'
            Pa = Paragraph('vnfdjksnvkjdsnkvnkdfsnbklgsvf四大皆空v那块地方是', style)
            Pa.wrapOn(p, 7 * inch, 10 * inch)
            Pa.drawOn(p, 0.5, 0.7 * inch)
            p.showPage()
            p.save()
            # response.write(note_obj.content)
            return response
        except Exception as e:
            print(e)
    # else:
    #     response = HttpResponse(content_type='application/md')
    #     response['Content-Disposition'] = 'attachment; filename="{}.md"'.format(quote(note_obj.note_name))
    #     response.write(html2text.html2text(note_obj.content))
    #     return response