import json
from django.http import JsonResponse
from activitys.models import UserInfo


def create_activity_check(func):
    def wrapper(self, request, *args, **kwargs):
        # 验证账户信誉积分是否足够
        data = request.body
        json_obj = json.loads(data)
        username = json_obj.get('user_name')

        if not username:
            result = {'code': 10301, 'error': '请登录/注册账号'}
            print('未登录账号')
            return JsonResponse(result)

        data = UserInfo.objects.filter(username=username)
        user_info = data[0]
        isActive = user_info.get('isActive')

        if isActive == False:
            result = {'code': 10302, 'error': '请激活您的账号'}
            print('账号未激活')
            return JsonResponse(result)

        credit = user_info.get('credit')
        if credit <= 85:
            result = {'code': 10303, 'error': '请提高您的信誉积分'}
            print('信誉积分不足')
            return JsonResponse(result)

        # login_days = user_info.get('login_days')
        # if login_days < 5:
        #     result = {'code': 10304, 'error': '没有权限创建活动,请登录5天以上再创建活动'}
        #     print('登陆天数不够')
        #     return JsonResponse(result)

        # result = {'code': 200, 'myuser': username}
        request.myuser = username

        return func(self, request, *args, **kwargs)
    return wrapper
