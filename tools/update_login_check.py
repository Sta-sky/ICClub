import jwt
from django.http import JsonResponse
from ICClub.settings import JWT_TOKEN_KEY
from users.models import UserRegist


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        # 获取用户的token
        token = request.META.get('HTTP_AUTHORIZATION')
        print('22222222222')
        print(token)
        # 判断用户是否拥有token
        if not token:
            return JsonResponse({'code': 10101, 'message': '请先登录'})
        res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        username = res['username']
        # 获取用户id
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'code': 10102, 'message': '页面不存在'})
        # 获取用户对象
        try:
            user = UserRegist.objects.filter(id=user_id)[0]
            # 判断是否是本人登录
            if username == user.username:
                request.myuser = user
            else:
                return JsonResponse({'code': 10103, 'message': '你无权查看该页面'})
        except Exception as e:
            print(e)

        return func(self, request, *args, **kwargs)

    return wrapper
