import jwt
from django.http import JsonResponse
from ICClub.settings import JWT_TOKEN_KEY
from users.models import UserRegist
from tools.response_code import code


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        # 获取用户的token
        try:
            print('///////')
            token = request.META.get('HTTP_AUTHORIZATION')
            print(token)
        except Exception as e:
            print('============')
            return JsonResponse(code[10200])
        # 判断用户是否拥有token
        # 如果有正常登录  如果没有  返回错误代码  前端跳转到登录页面
        if token == 'null':
            return JsonResponse(code[10203])
        try:
            res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            return JsonResponse(code[10204])
        username = res['username']
        try:
            user = UserRegist.objects.get(username=username)
        except Exception as  e:
            print(e)
            return JsonResponse({'code': 11111})
        request.myuser = user
        return func(self, request, *args, **kwargs)

    return wrapper
