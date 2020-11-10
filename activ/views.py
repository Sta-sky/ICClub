import base64
import pickle
import random
import time
from urllib import parse
import re
from threading import Thread
# from django.shortcuts import render
# Create your views here.get_redis_connection
import jwt
from django.db.models import F
from django_redis import get_redis_connection
from haystack.inputs import Raw
from haystack.query import SearchQuerySet

from ICClub.settings import JWT_TOKEN_KEY
from tools import chang_imgname
from activ.models import UserInfo, AdminArticle
from tools.static_data import ActiveUserData, AdminArticleData
from users.models import UserRegist
from response_code import code
from tools.logging_checked import login_check
from dwebsocket.decorators import accept_websocket
# from django.http import HttpResponse, Http404

from django.conf import settings
from haystack.forms import ModelSearchForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from activ.models import Activity, InterestTag
import json

# # Create your views here.
from django.views.generic.base import View


class Active(View):
    # 请求活动信息
    # @accept_websocket
    # @create_activity_check
    def get(self, request, state):

        # 如果是websocket协议连接
        if request.is_websocket():

            request.websocket.send('活动最新信息'.encode())
        else:
            return JsonResponse('随便发几个意思一下')

    # 创建活动
    # @create_activity_check
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
        data = request.body
        res = json.loads(data)
        if not data:
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
            print('tag')
            print(tag)
            print(type(interest))
            print(interest)
        except Exception as e:
            print(e, '活动标签查询异常')
            return JsonResponse(code[10002])

        img = interest.img_url.name
        print('图片测试来了')
        user = request.myuser
        try:
            act = Activity.objects.create(user=user, tag=interest, subject=title, content=content,
                                          status=1, act_img=img, end_time=endtime, beg_time=starttime,
                                          condition=condition)
        except Exception as e:
            print(e, '插入数据库异常')
            return JsonResponse(code[10001])
        print('\33[36m测试中间段输出[0m\33')
        try:
            file = res.get('img', '')
            if file:
                file = file.split(',')
                files = base64.b64decode(file[1])
                imgtext = file[0]
                # data:image/jpeg;base64  data:image/jpeg;base64
                img = re.findall(r'^.+?/(.+?);base64', imgtext)[0]
                filename = '%d.' % act.id + img
                print('活动文件保存地址')
                print(filename)
                if self.save(files, filename):
                    act.act_img = settings.DBACTIMG + filename
                    act.save()
            newact = get_redis_connection('newact')
            newact.delete('new_act' + act.tag.interests)
            newact.delete('new_act')
            user_list = [act.user.email]
            user_lists = json.dumps(user_list)
            activity = get_redis_connection('activity')
            try:
                activity.hset(act.id, act.created_time.strftime('%Y-%m-%d'), user_lists)
                activity.expire(act.id, 60 * 60 * 24)
            except Exception as e:
                print('redis写入失败', e)
                act.delete()
                return JsonResponse(code[10005])
            settings.ACTIVITY_NUM += 1
            userinfos = UserInfo.objects.get(id=user.userinfo.id)
            userinfos.sponsor_num = userinfos.sponsor_num + 1
            # user.sponsor_num = user.sponsor_num + 1
            userinfos.save()
            # act.user.userinfo.sponsor_num = F('sponsor_num') + 1
            # print("\033[36m发布活动数（后）：\033[0m")
            result = {'code': 200, 'actid': act.id}
        except Exception as e:
            print(e)
            act.delete()
            return JsonResponse(code[201])
        return JsonResponse(result)

    def save(self, save_file, name):
        filename = settings.ACTIMAGE_DIR + name
        print('////////44444444444444')
        print('活动文件保存路径')
        print(filename)
        with open(filename, 'wb') as f:
            f.write(save_file)
            print(filename, '已写入', name)
        return True


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
        print(activity)
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
        if len(content) > 80:
            content = content[:80] + '...'
        if len(title) > 12:
            title = title[:12] + '...'
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
    print('页码')
    print(request.get_full_path())
    print(request.path_info)
    print(page)
    """
    获取主页跟标签页的最新活动信息 优先读取djredis
    按时间排序 筛选最近发布的活动
    把前80 名 放进django-redis
    按每8条数据分页
    把对应page的内容返回
    :return:
    """
    if request.method == 'GET':
        print('传达出的撒长达')
        print('进来了')
        label = request.GET.get('tag', '')
        print(label, '**********')
        act_now_num = settings.ACTIVITY_NUM
        if request.is_websocket():
            redname = 'new_act' + label
            newact = get_redis_connection('newact')
            print('??????>>>>>>>>>>>>>>>')
            print(newact)
            # TODO 此处优化redis中拿去数据 ，要跟mysql中同步，
            # if newact.exists(redname):
            #     paginator = pickle.loads(newact.get(redname))
            #     print(paginator)
            #     result = make_result(paginator, page)
            # else:
            result = get_result(page, label)
            if not result:
                result = code[201]
            request.websocket.send(json.dumps(result))

            while True:
                # 备用 页面切换
                if request.websocket.has_messages():
                    print('连接关闭')
                    request.websocket.close()
                    return JsonResponse(code[201])

                # 检查是否有新消息
                if settings.ACTIVITY_NUM > act_now_num:
                    act_now_num = settings.ACTIVITY_NUM
                    result = get_result(page, label)
                    request.websocket.send(json.dumps(result))
                time.sleep(1)
        return JsonResponse(code[10202])


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
            return JsonResponse(code[201])
        paginator = Paginator(activity, 8)
        # TODO 把pagintor存放在redis中
        act_list = paginator.page(page)
        numpages = paginator.num_pages
        now_page = act_list.number
        data = []
        for act in act_list:
            content = act.content
            title = act.subject
            if len(content) > 80:
                content = content[:80] + '...'
            if len(title) > 12:
                title = title[:12] + '...'
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


class ActIndexView(View):
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
        all_list = Activity.objects.all().order_by('-click_nums')[:3]
        # 1. 首页最新活动默认显示三个
        index_data = []
        # acts = all_list[0]
        # print('data',acts)
        for item in all_list:
            # print('item', item)
            # print(type(item))
            index = {}
            index['act_id'] = str(item.id)
            index['subject'] = item.subject
            imgname = chang_imgname.parse_imgname(item.act_img.name)
            index['imgurl'] = imgname

            index_data.append(index)
        # index_img = json.loads(index_data)
        result = {"code": 200, "data": index_data}
        return JsonResponse(result)


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
    # print('set_users2:', len(set_users2))
    # print(88888888888888)
    set_active_users = set_users1 | set_users2  # miao!

    # 调试时传送静态数据在前端显示，数据库有数据时可以注释
    # if 1 or len(users1) < 8 or len(users2) < 8 or set_active_users is None or len(set_active_users) < 8:
    #     data = ActiveUserData
    #     result = {'code': 200, 'data': data}
    #     return JsonResponse(result)

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

    # print("向前端传送用户数量：", len(data))
    # for dic in data:
    #     print('----------------------------')
    #     print(dic)

    # response={'code':200,data:{active_user,...}}
    result = {'code': 200, 'data': data}
    return JsonResponse(result)
    # return render(request, 'oto/index.html', locals())


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
    # print('users1:', len(users1))
    if len(users1) > 10:
        set_users1 = set(users1[:10])
    else:
        set_users1 = set(users1)
    # print('set_users1:', len(set_users1))
    # 从数据库获取参与活动前60名
    users2 = UserInfo.objects.order_by('-participate_num')
    # print('users2:', len(users2))
    if len(users2) > 10:
        set_users2 = set(users2[:10])
    else:
        set_users2 = set(users2)
    # print('set_users2:', len(set_users2))
    # print(88888888888888)
    set_active_users = set_users1 | set_users2

    # # 调试时传送静态数据在前端显示，数据库有数据时可以注释
    # if 1 or len(users1) < 8 or len(users2) < 8 or set_active_users is None or len(set_active_users) < 8:
    #     data = ActiveUserData
    #     result = {'code': 200, 'data': data}
    #     return JsonResponse(result)

    users_data = []
    # 从redis中获取所有数据
    redis_conn = get_redis_connection('users')
    redis_index = redis_conn.get('active_users')

    # 判断内存中有无数据
    if redis_index is None:
        print("未使用缓存")
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
        # redis_conn.ex ()
        # print(222222222222)
        # 获取集合中元素数量
        # print(redis_index.llen('active_users'))*
    else:
        print("使用缓存 >>>>>>>>>>>>>>>." )
        users_data = json.loads(redis_index)

    # 从集合中随机取8个用户
    if len(users_data) >= 8:
        data = random.sample(users_data, 8)
    else:
        data = users_data

    # print(333333333333333)
    # print("向前端传送用户数量：", len(data))
    # for dic in data:
    #     print('----------------------------')
    #     print(dic)

    # response={'code':200,data:{active_user,...}}
    result = {'code': 200, 'data': data}
    return JsonResponse(result)


# 优先从redis中获取数据，redis中没有数据则从MySQL获取数据
def get_admin_articles(request):
    """
    用Django-redis实现
        从官方文件中获取最新4篇文章，展示在主页窗口的第一屏
    """

    # 127.0.0.1:8000/v1/activ/article

    # 从数据库获取管理员发布的最新四篇文章
    try:
        admin_user = UserRegist.objects.get(id=5)
        print('》》》》》》》》》》》》》》》》》》')
        print(admin_user)
        # print(admin_user)
        obj_articles = AdminArticle.objects.filter(user=admin_user).order_by('updated_time')[:4]
        # obj_articles = AdminArticle.objects.filter(id=5)
        print(obj_articles)
        print('obj_article:', len(obj_articles))
    except Exception as e:
        print("管理员用户数据取出错误：", e)
        return JsonResponse({'code': 201, 'error': '没有活动'})


    # 调试时传送静态数据在前端显示，数据库有数据时可以注释
    # if 1:
    #     data = AdminArticleData
    #     result = {'code': 200, 'data': data}
    #     return JsonResponse(result)

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
            article_info['content'] = article.content[:90] + '...'
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

    # print(len(article_data))
    # for dic in article_data:
    #     print('----------------------------')
    #     print(dic)

    # response={'code':200,data:{article_info,...}}
    result = {'code': 200, 'data': article_data}
    return JsonResponse(result)


def article_info(request):
    article_id = request.GET.get('article_id')
    print('>文章的>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('文章的  啊啊啊啊article_id:', article_id)
    if not article_id:
        return JsonResponse({'code': 404, 'message': '页面不存在'})
    try:
        article = AdminArticle.objects.get(id=article_id)
    except Exception as e:
        print(e)
        result = {'code': 404, 'message': '文章不存在'}
        return JsonResponse(result)

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
        :param request:
        :return:
        """
        # 获取act_id
        data = request.body
        data = json.loads(data)
        print('>>>>>>>>>>>>>')
        print(data)
        act_id = int(data.get('act_id'))
        if act_id is None:
            result = {'code': 10405, 'error': '活动未找到'}
            print('活动未找到, >>>>>>>>>>.')
            return JsonResponse(result)
        try:
            act = Activity.objects.get(id=act_id)
            act.click_nums  = act.click_nums + 1
            act.save()
        except Exception as e:
            result = {'code': 10404, 'error': '活动未找到'}
            print(f'活动未找到, $$$$$$$$$$$$$$$$${e}')
            return JsonResponse(result)
        act = act
        result = {"code": 200, 'subject': act.subject, 'content': act.content,
                  'starttime': act.beg_time.strftime('%Y-%m-%d'),
                  'like': act.likes}
        return JsonResponse(result)


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 8)

def activitySearchView(request, load_all=True, form_class=ModelSearchForm, searchqueryset=None, extra_context=None, results_per_page=None):
        """首⻚查询功能"""
        # 127.0.0.1:8000/active/search/1
        data = request.POST.get('q')
        print('*' * 50)
        print(data)
        if not data:
            return JsonResponse({'code': 40003, 'error': '没有检索到关键字'})
        form = ''
        try:
            form = ModelSearchForm(request.POST, load_all=True)
        except Exception as e:
            print(e)
        print(form)
        if form.is_valid():
            # results = form.search().highlight()
            results = form.search()
        else:
            return JsonResponse({'code': 40002, 'error': 'form表单数据错误'})
        print(655 ,results.all())
        # print('--------------------------------')
        # sqs = SearchQuerySet().filter(content=data)
        # print(sqs)

        tag = request.POST.get('tag', '')
        print('=================')
        print(tag)
        if (tag):
            lab = parse.unquote(tag)
            print('进来了')
            try:
                obj = InterestTag.objects.get(interests=lab)
                results = results.filter(tag=obj.id)
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            except Exception as e:
                print(e, '非法标签')
                result = {'code': 10006, 'error': '非法值'}
                return JsonResponse(result)

        page_size = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE
        paginator_obj = Paginator(results, page_size)
        print(paginator_obj)
        print(']]]]]]]]]]]]]]]]]]]]]]]]]')
        print(page_size)
        try:
            # 当前页的对象

            ress = []
            print(705 ,ress)
            current_page = paginator_obj.page(pgnow)
            print(current_page)
            print(type(current_page))
            for i in current_page:
                print('###############')
                ress.append(i.subject)
            # 获取页码总数
            allpage = paginator_obj.num_pages
            print(allpage)
            print(type(allpage))
            print(type(pgnow))
        except Exception as e:
            print(e)
            result = {'code': 40001, 'error': '⻚数有误,小于0或者大于总⻚数'}
            return JsonResponse(result)
        activity_list = []
        print(713 ,current_page.object_list)
        for result in current_page.object_list:
            print('[[[[[[[[[[[[[[[===========')
            act = {}
            content = result.object.content
            title = result.object.subject
            if len(content) > 80:
                content = content[:80] + '...'
            if len(title) > 12:
                title = title[:12] + '...'
            act['act_id'] = result.object.id
            act['subject'] = title
            act['content'] = content
            # 获取活动需要的信息
            tag = int(result.object.tag_id)
            tag = InterestTag.objects.filter(id=tag)
            act['tag'] = tag[0].interests
            act['imgurl'] = result.object.act_img.name
            act['date'] = result.object.created_time.strftime('%Y-%m-%d')

            activity_list.append(act)

        result = {"code": 200,
                  "data": activity_list,
                  'page': [int(pgnow), allpage]
                  }
        print(result)
        return JsonResponse(result)