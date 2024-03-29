import json
import base64
from django.http import JsonResponse
from activitys.models import UserInfo, InterestTag, Activity
from tools.response_code import code
from tools.util import DateEnconding, upload_img_save, judge_token_expire
from users.models import UserRegist
from ICClub import settings


def user_info(request):
    """
    用户信息详情获取
    :param request:
    :return:
    """
    data = {}
    # 获取用户的token
    token = request.META.get('HTTP_AUTHORIZATION')
    # 判断用户是否拥有token
    print('进来了')
    if token == 'null':
        # 没有token
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 404, 'message': '页面不存在'})
        # 不是本人登录
        data['is_self'] = 'no'
        # 从数据库中提取数据
        res_data = get_date(data=data, user_id=user_id)
        data = json.loads(json.dumps(dict(res_data), cls=DateEnconding))
        result = {'code': 200, 'data': data}
        print('NOT 本人 登录返回')
        return JsonResponse(result, safe=False)
    # 有token 用户已登录
    elif token:
        print('token')
        res = judge_token_expire(token)
        if not res:
            return JsonResponse(code[10201])
        username = res['username']
        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse(code[10205])
        # 获取用户对象
        try:
            user_1 = UserRegist.objects.filter(id=user_id)[0]
            # 判断是否是本人登录
            if username == user_1.username:
                data['is_self'] = 'yes'
            else:
                data['is_self'] = 'no'
        except Exception as e:
            print(e)
            return JsonResponse(code[10205])
        # 从数据库中提取数据
        res_data = get_date(data=data, user_id=user_id)
        data = json.loads(json.dumps(dict(res_data), cls=DateEnconding))
        code[200]['data'] = data
        return JsonResponse(code[200], safe=False)


# 获取用用户信息
def get_date(data, user_id):
    try:
        user_info = UserInfo.objects.get(user_id=user_id)
    except Exception as e:
        print(e, '3333333333')
        return {'code': 10122, 'message': '该用户不存在'}
    user_dic = {}
    user_dic["nickname"] = user_info.nickname
    user_dic["introduction"] = judge_null_data(user_info.introduction)
    user_dic["gender"] = judge_null_data(user_info.gender)
    if not user_info.birth:
        user_dic["birth"] = user_info.created_time.strftime('%Y-%m-%d')
    else:
        user_dic["birth"] = user_info.birth.strftime('%Y-%m-%d')
    user_dic["city"] = judge_null_data(user_info.city)
    user_dic["url"] = user_info.portrait.name
    user_dic["credit"] = user_info.credit
    user_dic["level"] = user_info.level
    user_dic["logins_days"] = cal_num(user_info.login_days)
    user_dic["sponson_num"] = cal_num(user_info.sponsor_num)
    user_dic["participat_num"] = cal_num(user_info.participate_num)
    user_dic["likes"] = cal_num(user_info.likes)
    user_dic["interest"] = []
    for i in user_info.interest.all():
        user_dic['interest'].append(('%s ' % i.interests))
    # 发起的活动
    # 获取对象发起的所有活动
    data['user_info'] = user_dic
    try:
        act_list = []
        user_act = Activity.objects.filter(user_id=user_id).order_by('-created_time')[:10]
        data = get_active_join(data=data, user_info=user_info)
        for i in user_act:
            act_dic = {}
            act_dic["act_id"] = i.id
            act_dic["tag"] = i.tag.interests
            act_dic["subject"] = i.subject
            act_dic["create_time"] = str(i.created_time.date())
            act_dic["click_num"] = cal_num(i.click_nums)
            act_dic["update_time"] = str(i.updated_time.date())
            act_dic["status"] = i.status
            act_list.append(act_dic)
        data['create_act_info'] = act_list
    except Exception as e:
        print(e)
        return {'code': 10111, 'message': e}
    return data


def get_active_join(data, user_info):
    # 获取该用户对象参与的所有活动对象
    try:
        user_part = user_info.activityparticipant_set.all()
        act_list = []
        for up in user_part:
            act_dic = {}
            act_dic["act_id_p"].append(up.activity.id)
            act_dic["tag_p"].append(up.activity.tag.interests)
            act_dic["subject_p"].append(up.activity.subject)
            act_dic["create_time_p"].append(up.created_time)
            act_dic["click_num_p"].append(up.activity.click_nums)
            act_dic["update_time_p"].append(up.updated_time)
            act_dic["collection"].append(up.activity.collection)
            act_list.append(act_dic)
        data['join_act_info'] = act_list
    except Exception as e:
        return {'code': 10112, 'message': e}
    return data

def judge_null_data(data):
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


# @login_check
def update_user_info(request):
    # 获取用户的token
    token = request.META.get('HTTP_AUTHORIZATION')
    print(token)
    print('*' * 50)
    # 判断用户是否拥有token
    if token == 'null':
        return JsonResponse(code[10203])
    res = judge_token_expire(token)
    if not res:
        return JsonResponse(code[10201])
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
                code[200]['data'] = data1
                return JsonResponse(code[200])
            else:
                return JsonResponse(code[10206])
        except Exception as e:
            print(e)
            return JsonResponse(code[10205])

    if request.method == "POST":
        print('post...............')
        # 获取上传数据
        data = request.body
        if not data:
            code[10207]['message'] = '没有数据传输'
            return JsonResponse(code[10207])
        # 转换为json格式
        json_data = json.loads(data)
        # 获取具体数据 并赋值
        nickname = json_data.get('nickname')
        signature = json_data.get('signature')
        gender = json_data.get('gender')
        birth = json_data.get('birth')
        pro = json_data.get('pro')
        city = json_data.get('city')
        interests = json_data.get('interest')
        print('posy...........')
        print(birth)

        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            code[10207]['message'] = '页面不存在'
            return JsonResponse(code[10207])
        # 判断用户昵称是否重复
        try:
            user_1 = UserInfo.objects.filter(nickname=nickname)
            if user_1[0] != UserInfo.objects.get(user_id=user_id):
                code[10207]['message'] = '昵称已存在'
                return JsonResponse(code[10207])
        except Exception as e:
            print(e)
            return JsonResponse(code[10205])
        # 获取用户对象
        try:
            user_2 = UserRegist.objects.filter(id=user_id)[0]
            # 判断是否是本人登录
            if username == user_2.username:
                # 更新数据库数据
                user = UserInfo.objects.filter(user_id=user_id)
                user.update(nickname=nickname, introduction=signature,
                            gender=gender, birth=birth, city=pro + city)
                user[0].interest.clear()
                if len(interests) == 0:
                    return JsonResponse(code[200])
                for interest in interests:
                    user_interest = InterestTag.objects.get(interests=interest)
                    user[0].interest.add(user_interest.id)
                return JsonResponse(code[200])
        except Exception as e:
            print(e)
            code[10207]['message'] = e
            return JsonResponse(code[10207])




# 上传图片
def upload_img(request):
    print(request.method)
    if request.method == 'POST':
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse(code[10203])
        res = judge_token_expire(token)
        if not res:
            return JsonResponse(code[10201])
        username = res['username']
        # 获取图片数据
        json_data = request.body
        data = json.loads(json_data)
        file = data.get('data').split(',')
        img_data = base64.b64decode(file[1])
        # 服务器本地存储路径+图片名
        file_path = settings.USERIMAGE_DIR + username + settings.IMG_END
        # 将上传的头像存储到本地
        save_res = upload_img_save(img_data, file_path)
        if save_res['code'] == 10501:
            print(save_res['message'])
            return JsonResponse(code[10501])
        # 通过token 获取登录对象 并添加头像的本地存储路径
        else:
            user = UserRegist.objects.filter(username=username)[0]
            user.userinfo.portrait = settings.DBUSEIMG + username + settings.IMG_END
            user.userinfo.save()
        code[200]['message'] = '头像修改成功'
        return JsonResponse(code[200])

