import json
import random

from django.conf import settings
from django.http import JsonResponse

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from activitys.models import InterestTag, Activity
from tools.response_code import code
from tools.logging_checked import login_check
from celery_tasks.user_celery import send_active_mail
from tools.recommend import getALLDataStruct, recommendList


class Label(View):
    @login_check
    def get(self, request, id):
        """
        参与活动 活动投票
        SISMEMBER key member 查看是否已经加入活动
        获取活动id,用户id,存储在django-redis(activitys)中
        :return:
        """
        print('进来了')
        try:
            time = request.GET.get('date')

        except Exception as e:
            print(e, '没有获取到有效参数')
            return JsonResponse(code[10004])
        activity = get_redis_connection('activitys')
        try:
            user_list_js = activity.hget(id, time)
            user_list = json.loads(user_list_js)
        except Exception as e:
            user_list = []
        try:
            active = Activity.objects.get(id=id)
        except Exception as e:
            print('警告！，redis数据库出现错误')
            return JsonResponse(code[10002])
        user = request.myuser
        user_list.append(user.email)
        # option('#@#@@#@#@#@#@#')
        # print(len(user_list))
        activity.hset(id, time, json.dumps(user_list))
        settings.ACTCONDITION.append(active.id)
        # print(settings.ACTCONDITION)
        if len(user_list) >= active.condition:
            # print(active.condition)
            redis = get_redis_connection('activitys')
            # TODO 活动达成，调用给所有用户发邮件方法
            for id in settings.ACTCONDITION:
                try:
                    user_email_js = redis.hget(id, time)
                    # print(user_email_js)
                except Exception as  e:
                    print(e)
                    result = {'code': 10201, 'message': 'rdis获取数据错误'}
                    return JsonResponse(result)
                user_email_list = json.loads(user_email_js)
                for email in user_email_list:
                    # print(email)
                    # print('$$$$$$$$$$$$4')
                    title = active.subject
                    start_time = str(active.beg_time)
                    end_time = str(active.end_time)
                    data = '活动从' + start_time + '开始' + '到' + end_time + "结束"
                    send_active_mail.delay(email, title, data)
            active.status = 2
            active.save()

            return JsonResponse({'code': 200, 'data': '活动条件达成,活动即将开始'})
        return JsonResponse(code[200])

    @login_check
    def post(self, request):
        """
        获取标签
        获取用户爱好标签
        如果有 取出标签返回  不够8个就补
        如果没有 随便从标签表中取出8个返回
        :param request:
        :return:
        """

        # {'游戏': 1,
        #   '机车': 1,
        #   'IT': 1,
        #   '二次元': 1,
        #   '足球': 0.558488658476091,
        #   '跑步': 0.558488658476091,
        #   '篮球': 0.558488658476091,
        #   '美食': 0.558488658476091,
        #   '舞蹈': 0.558488658476091,
        #   '爬山': 0.558488658476091,
        #   '音乐': 0.558488658476091}

        all_user_act = getALLDataStruct()
        # print('#################')
        # print(all_user_act)

        user = request.myuser
        uid = user.id
        print('@@@@@@@@@@@@@@@@@')
        print('目标用户uid', uid)
        label_list = []

        recomLabel = recommendList(all_user_act, uid)
        print('@@@@recomLabel@@@@@@@@')
        print(recomLabel)
        if recomLabel != []:
            inst = list(recomLabel.keys())
            if len(inst) < 4:
                label_list = random.sample(inst, len(inst))
            else:
                label_list = random.sample(inst, 4)

        lab_list = InterestTag.objects.all()[:100]
        print('///////////////////////////////')
        print(lab_list)
        if len(label_list) < len(lab_list):
            # 不够8个标签补齐
            length = len(lab_list)
            while len(label_list) < 8:
                lab = lab_list[random.randint(0, length - 1)].interests
                if lab not in label_list:
                    label_list.append(lab)

        result = {'code': 200, 'data': label_list}
        return JsonResponse(result)


class LabelHotView(View):
    def get(self, request):
        pass

    def post(self, request):
        """
        最热活动展示
        最热： 点击量 收藏 综合排名前三
        先读django-redis  没有再查数据库
        保存数据 过期时间
        """
        # 0. 获取所有品类
        data = request.body()
        data = json.loads(data)
        tag = data.get('tag')
        print('tag')

        try:
            res = InterestTag.objects.filter(interests=tag)
        except Exception as e:
            result = {"code": 10400, "error": '未找到标签'}
            print('未找到标签')
            return JsonResponse(result)
        tag_id = res[0].id
        all_list = Activity.objects.filter(tag=tag_id).order_by('-click_nums')[:3]
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
            from tools import chang_imgname
            imgname = chang_imgname.parse_imgname(item.act_img.name)
            index['imgurl'] = imgname
            index_data.append(index)
        # index_img = json.loads(index_data)
        result = {"code": 200, "data": index_data}
        return JsonResponse(result)


def option(request):
    tag = InterestTag.objects.all()
    if not tag:
        return JsonResponse(code[201])
    res = []
    for val in tag:
        res.append(val.interests)
    result = {'code': 200, 'data': res}
    return JsonResponse(result)



class LabelLikeView(View):
    @login_check
    def post(self, request, status):
        act = request.body
        act = json.loads(act)
        act_id = act.get('actid')
        act_status = act.get('collection')
        if not act_id:
            return JsonResponse({'code': 10401, 'error': '未找到活动'})
        ap_file = Activity.objects.get(id=act_id)
        if status == 'collection':
            if act_status == '已收藏':
                ap_file.collection = ap_file.collection + 1
            elif act_status == '收藏':
                ap_file.collection = ap_file.collection - 1

        if status == 'like':
            ap_file.likes = ap_file.likes + 1

        ap_file.save()
        return JsonResponse({'code': 200, 'data': ap_file.likes})
