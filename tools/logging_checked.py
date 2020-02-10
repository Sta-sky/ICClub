import jwt
from django.http import JsonResponse
from ICClub.settings import JWT_TOKEN_KEY
from users.models import UserRegist
from response_code import code


def login_check(func):
    def wrapper(self, request, *args, **kwargs):

        # 获取用户的token

        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            # print('token:====',token)
        except Exception as e:
            print('not token')
            return JsonResponse(code[10200])
        # 判断用户是否拥有token
        # 如果有正常登录  如果没有  返回错误代码  前端跳转到登录页面
        if not token:
            result = {'code': 10204, 'message': '验证用户登录失败'}
            return JsonResponse(result)
        try:
            res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
            # print('resresresresresresresresres')
            # print(res)
        except Exception as e:
            print(e)
            result = {'code': 10204, 'message': 'token未通过  用户未登录'}
            return JsonResponse(result)
        username = res['username']
        # print('usernameusernameusernmae')
        # print(username)
        try:
            user = UserRegist.objects.get(username=username)
        except Exception as  e:
            print(e)
            return JsonResponse({'code': 11111})
        # print('11111111',user)
        request.myuser = user
        # request.username = username
        return func(self, request, *args, **kwargs)

    return wrapper
