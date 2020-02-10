import json
import time, re, base64

import jwt
from django.http import JsonResponse
from ICClub.settings import JWT_TOKEN_KEY
from activ.models import UserInfo, InterestTag, Activity
from users.models import UserRegist
from ICClub import settings


# todo toekn过期后逻辑尚未处理??????
def user_info(request):
    """
    用户信息详情获取
    :param request:
    :return:
    """
    data = {}
    # 获取用户的token
    token = request.META.get('HTTP_AUTHORIZATION')
    # print('进入用户信息')
    print(token)
    # 判断用户是否拥有token
    if token == 'null':
        # 没有token
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 404, 'message': '页面不存在'})
        # 不是本人登录
        data['is_self'] = 'no'
        # 从数据库中提取数据
        data = get_date(data=data, user_id=user_id)

        return JsonResponse(data)
    # 有token 用户已登录
    elif token:
        print('用户已登录,进入用户信息页面')
        res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        username = res['username']
        print(username)
        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 404, 'message': '页面不存在'})
        # 获取用户对象
        try:
            user_1 = UserRegist.objects.filter(id=user_id)[0]
            print(user_1.username)
            # 判断是否是本人登录
            if username == user_1.username:
                data['is_self'] = 'yes'
            else:
                data['is_self'] = 'no'

        except Exception as e:
            print(e)
        # 从数据库中提取数据
        print('11111111111111')
        data = get_date(data=data, user_id=user_id)
        return JsonResponse(data)


# @login_check
def update_user_info(request):
    # 获取用户的token
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)
    print('*' * 50)
    # 判断用户是否拥有token
    if token == 'null':
        print('8' * 50)
        return JsonResponse({'code': 10101, 'message': '请先登录'})
    res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
    username = res['username']

    if request.method == "GET":
        data1 = {}
        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 10102, 'message': '页面不存在'})
        # 获取用户对象
        try:
            user_2 = UserRegist.objects.filter(id=user_id)[0]
            inttag = InterestTag.objects.all()
            print(inttag)
            data1['tag'] = []
            for i in inttag:
                data1['tag'].append(i.interests)
            print(data1['tag'])
            # 判断是否是本人登录
            if username == user_2.username:
                print('2444444444444444')
                # 渲染数据库数据
                data1['nickname'] = user_2.userinfo.nickname
                data1['introduction'] = user_2.userinfo.introduction
                data1['gender'] = user_2.userinfo.gender
                data1['url'] = user_2.userinfo.portrait.name
                print(user_2.userinfo.birth)
                if not user_2.userinfo.birth:
                    data1['birth'] = user_2.userinfo.created_time.strftime('%Y-%m-%d')
                    print('??????????????')
                else:
                    data1['birth'] = user_2.userinfo.birth.strftime('%Y-%m-%d')
                data1['city'] = user_2.userinfo.city
                data1['interest'] = []
                for i in user_2.userinfo.interest.all():
                    data1['interest'].append(i.interests)
                print(data1)
                # data = json.dumps(data1)
                return JsonResponse({'code': 200, 'data': data1})

            else:
                return JsonResponse({'code': 10104, 'message': '你无权查看该页面'})
        except Exception as e:
            print('*' * 50)
            print(e)
            return JsonResponse({'code': 404, 'message': '用户不存在'})

    if request.method == "POST":
        print('post...............')
        # 获取上传数据
        data = request.body
        if not data:
            return JsonResponse({'code': 10105, 'message': '无数据传输'})
        # 转换为json格式
        json_data = json.loads(data)
        # 获取具体数据 并赋值
        nickname = json_data.get('nickname')
        signature = json_data.get('signature')
        gender = json_data.get('gender')
        birth = json_data.get('birth')
        pro = json_data.get('pro')
        city = json_data.get('city')
        interest = json_data.get('interest')
        print('posy...........')
        print(birth)

        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 10102, 'message': '页面不存在33'})
        # 判断用户昵称是否重复
        try:
            user_1 = UserInfo.objects.filter(nickname=nickname)
            if user_1[0] != UserInfo.objects.get(user_id=user_id):
                return JsonResponse({'code': 10120, 'message': '昵称已存在'})
        except Exception as e:
            print(e)
        # 获取用户对象
        try:
            user_2 = UserRegist.objects.filter(id=user_id)[0]
            # 判断是否是本人登录
            if username == user_2.username:
                # 更新数据库数据
                user = UserInfo.objects.filter(user_id=user_id)
                user.update(nickname=nickname, introduction=signature,
                            gender=gender, birth=birth, city=pro + city)
                # print('*' * 50)
                user[0].interest.clear()
                # print('老子来了')
                if len(interest) == 0:
                    return JsonResponse({'code': 200})
                for i in interest:
                    xq = InterestTag.objects.get(interests=i)
                    user[0].interest.add(xq.id)

                # print('老子又走了')
                return JsonResponse({'code': 200})

        except Exception as e:
            print(e)
            return JsonResponse({'code': 10111, 'message': e})

    print('233333333333333')
    return JsonResponse({'code': 10107, 'message': '未知错误'})


# 获取用用户信息
def get_date(data, user_id):
    try:
        user_info = UserInfo.objects.get(user_id=user_id)
        print(user_info)
    except Exception as e:
        print(e, '3333333333')
        return {'code': 10122, 'message': '该用户不存在'}
    # print(user_info.portrait)
    data['nickname'] = user_info.nickname
    data['introduction'] = jg_data(user_info.introduction)
    data['gender'] = jg_data(user_info.gender)
    if not user_info.birth:
        data['birth'] = user_info.created_time.strftime('%Y-%m-%d')
        print('??????????')
    else:
        data['birth'] = user_info.birth.strftime('%Y-%m-%d')
        print(data['birth'])
    data['city'] = jg_data(user_info.city)
    data['url'] = user_info.portrait.name
    data['credit'] = user_info.credit
    data['level'] = user_info.level
    data['logins_days'] = cal_num(user_info.login_days)
    data['sponson_num'] = cal_num(user_info.sponsor_num)
    data['participat_num'] = cal_num(user_info.participate_num)
    data['likes'] = cal_num(user_info.likes)
    data['interest'] = []
    for i in user_info.interest.all():
        data['interest'].append(('%s ' % i.interests))
    # 发起的活动
    # 获取对象发起的所有活动
    try:
        user_act = Activity.objects.filter(user_id=user_id).order_by('-created_time')[:10]
        print(user_act)
        data['act_id'] = []
        data['tag'] = []
        data['subject'] = []
        data['create_time'] = []
        data['click_num'] = []
        data['update_time'] = []
        data['status'] = []
        if len(user_act) == 0:
            data = get_active_join(data=data, user_info=user_info)
            return data
        for i in user_act:
            data['act_id'].append(i.id)
            data['tag'].append(i.tag.interests)
            data['subject'].append(i.subject)
            data['create_time'].append(str(i.created_time.date()))
            data['click_num'].append(cal_num(i.click_nums))
            data['update_time'].append(str(i.updated_time.date()))
            data['status'].append(i.status)
    except Exception as e:
        print(e)
        return {'code': 10111, 'message': e}
    data = get_active_join(data=data, user_info=user_info)
    return data


def get_active_join(data, user_info):
    # 获取该用户对象参与的所有活动对象
    try:
        user_part = user_info.activityparticipant_set.filter().order_by('-created_time')[:10]
        print(user_part)
        data['act_id_p'] = []
        data['tag_p'] = []
        data['subject_p'] = []
        data['create_time_p'] = []
        data['click_num_p'] = []
        data['update_time_p'] = []
        data['status_p'] = []
        if len(user_part) == 0:
            print('kong   00000000000000')
            return {'code': 200, 'data': data}
        for up in user_part:
            data['act_id_p'].append(up.activity.id)
            data['tag_p'].append(up.activity.tag.interests)
            data['subject_p'].append(up.activity.subject)
            data['create_time_p'].append(up.created_time)
            data['click_num_p'].append(up.activity.click_nums)
            data['update_time_p'].append(up.updated_time)
            data['collection'].append(up.collection)
    except Exception as e:
        print(e)
        return {'code': 10112, 'message': e}
    return {'code': 200, 'data': data}


def jg_data(data):
    if not data:
        return ''
    return data


def cal_num(num):
    if int(num) > 10000:
        new_num = str(int(num) // 10000) + 'w'
        return new_num
    elif int(num) > 1000:
        new_num = str(int(num) // 1000) + 'k'
        return new_num
    else:
        return num


# 上传图片测试
def upload_test(request):
    print(request.method)
    if request.method == 'POST':
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        username = res['username']
        # 获取图片数据
        json_data = request.body
        data = json.loads(json_data)
        file = data.get('data').split(',')
        img = base64.b64decode(file[1])
        # 用正则匹配出图片文件格式
        img_end = re.findall(r'^.+?/(.+?);base64', file[0])[0]
        # 服务器本地存储路径+图片名
        filename = settings.USERIMAGE_DIR + username + '.' + img_end

        # 通过token 获取登录对象 并添加头像的本地存储路径
        user = UserRegist.objects.filter(username=username)[0]
        user.userinfo.portrait = settings.DBUSEIMG + username + '.' + img_end
        user.userinfo.save()
        # 将上传的头像存储到本地
        with open(filename, 'wb') as f:
            f.write(img)
        return JsonResponse({'code': 200, 'message': '收到'})
    return JsonResponse({'code': 200, 'message': '??????????'})

#
# class Users(View):
#     def get(self, request):
#         return
#
#     def post(self, request):
#         return
#
#
# # 发邮件 邮件验证地址+收件人eamil
# def send_active_mail(code_url, email):
#     subject = '达达商城用户激活邮件'
#     html_message = """
#         <p>尊敬的大人，您好</p>
#         <p>激活链接为<a> href='%s' target='blank'>点击激活</a></p>""" % code_url
#     send_mail(subject, '', settings.SYSEMAIL, html_message=html_message, recipient_list=[email])
#
#
# # 首页活跃达人栏Ajax测试
# def active_user(request):
#     """
#         活动达人数据后端集orderBy(发起活动数×10+参与活动数×8).limit(降序前100)
#         从数据库获取发起活动数和参与活动数
#         注意：在用户信息表里创建了发起活动和参与活动字段
#             1.需要用户在创建活动时+1，删除活动时-1
#             2.用户参与活动时+1
#     """
#     #
#     obj_active_users = UserInfo.objects.all().order_by('sponsor_num')[:100]
#     active_users = random.choices(obj_active_users, 8)
#     for user in active_users:
#         user_id = user.id
#         nicknames = user.nicknames
#         gender=user.gender
#         hd_pic=user.portrait
#         # sign_words=
#         hd_pic = '../static/images/img02-3.png'
#         sign_words = user.introduction
#         # 发起活动数
#         sponsor_num = user.sponsor_num
#         # 参与活动数
#         participate_num = user.participate_num
#         tags = user.interest  # 取
#
#     nicknames = ['运动达人1', '运动达人2', '运动达人3', '运动达人4', '运动达人5', '运动达人6', '运动达人7', '运动达人8']
#     gender1 = 1
#     gender2 = 2
#     hd_pic = '../static/images/img02-3.png'
#     sign_words = '我运动我快乐，我健康，和我一起运动吧！！！'
#     # 发起活动数
#     sponsor_num = 192
#     # 参与活动数
#     participate_num = 88
#     tags = ['跑步', '旅游', '摄影']
#
#     data = []
#     for i in range(8):
#         if i % 2 == 0:
#             gender = gender1
#         else:
#             gender = gender2
#         data.append({
#             'user_id': user_id + i,
#             'nickname': nicknames[i],
#             'gender': gender,
#             'hd_pic': hd_pic,
#             'sign_words': sign_words,
#             # 发起活动数
#             'sponsor': sponsor_num,
#             # 参与活动数
#             'participate': participate_num,
#             # 兴趣标签，取前3个
#             'tags': tags
#         })
#
#     # response={'code':200,data:{active_user,...}}
#     result = {'code': 200, 'data': data}
#     return JsonResponse(result)
# # -------------------------------------------------------------------
