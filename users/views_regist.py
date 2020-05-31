import base64
import json
import random
import re
from urllib.parse import urlencode
import jwt
import time
import hashlib
import redis
import requests
from django.conf import settings
#   事务
from django.db import transaction
from django.http import  JsonResponse
from django.shortcuts import render
from celery_tasks.user_celery import send_act_email

from activ.models import UserInfo
from users.models import UserRegist, WeiboUser

r = redis.Redis(host='localhost', port='6379', db=1)
s = redis.Redis(host='localhost', port='6379', db=3)


# 网站用户注册
def regist_view(request):
    if request.method == "GET":
        return render(request, '../templates/dyy/../regist.html')

    if request.method == 'POST':

        # 前端使用了stringify  转换成了json的字符串 所以  需要loads（）一下  转换成json对象
        data = request.body
        print(data)
        # 将json字符串转换成为 接送对象
        json_data = json.loads(data)
        print('++++++++++++++++')
        print(json_data)
        # 判断前端传过来的数据是否存在
        if not json_data:
            return JsonResponse({'code': 10200, 'message': 'request data  format is error'})
        # 再次逐个判断前端传来的数据存在
        # TODO  邮箱正则
        # 定义 判断邮箱地址的正则

        username = json_data.get('username')
        password = json_data.get('password')
        passwords = json_data.get('passwords')
        email = json_data.get('email')
        phone = json_data.get('phone')
        user_code = json_data.get('code')
        if not username and not password and not passwords and not phone and not user_code:
             return JsonResponse({'code': 10200, 'message':  '注册信息不完整'})
        if email_check(email) == False:
            return JsonResponse({'code': 10200, 'message':  '邮箱格式错误 '})

        # TODO 此处加手机验证码 判断
        # try:
        #     # 取出code核对
        #
        #     redis_code = s.hget(username,phone)
        #     print(redis_code)
        #     print('$#$#$#$#$###########')
        #     redis_code = json.loads(redis_code)
        #     print(redis_code)
        # except Exception as e:
        #     print(e)
        #     result = {'code': 10223, 'message': 'redis用户不存在'}
        #     return JsonResponse(result)
        # if user_code != redis_code:
        #     result = {'code': 10224, 'message': '验证码错误,'}
        #     return JsonResponse(result)

        # 验证完 删除对应的code
        # s.hdel(username,phone)


        # 密码加密
        # 判断两次密码是否一致

        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()

        ms = hashlib.md5()
        ms.update(passwords.encode())
        passwords = ms.hexdigest()

        if passwords != password:
            result = {'code': 10200, 'message': '两次密码不一致'}
            return JsonResponse(result)
        # 从数据库中过滤  是否已经有了前端传来的username
        user = UserRegist.objects.filter(username=username)

        #   用户已经存在 返回
        if user:
            result = {'code': 10201, 'message': '用户名已经存在,请换个昵称试试'}
            return JsonResponse(result)
        # 用户存在创建用户
        try:
            user = UserRegist.objects.create(username=username, password=password, email=email,
                                             phone=phone, code=user_code)
            UserInfo.objects.create(nickname=username, user_id=user.id)
        except Exception as e:
            print(e, '用户创建失败')
            result = {'code': 10210, 'message': '注册信息错误'}
            return JsonResponse(result)

        # 签发token
        token = make_token(username)
        # TODO 激活邮件
        random_num = random.randint(1000, 9999)
        code_random = username + '_' + str(random_num)
        base_code = base64.urlsafe_b64encode(code_random.encode()).decode('utf-8')
        # 将数据存入缓存中  等待用户发送请求验证  激活
        r.set('email_code%s' % username, base_code)

        email_url = 'http://176.209.104.17:7001/templates/email_activ.html?code=%s' % base_code
        print(email_url)
        try:
            send_act_email.delay(email, email_url)
            print('###########')
        except Exception as e:

            print(e)
            result = {'code':10220,'message':'邮箱发送失败 !请核对邮箱'}
            return JsonResponse(result)
        print('进来了222222')

        result = {'code': 200, 'username': username, 'id': user.id, 'token': token.decode()}
        print('@@@@@@@@@@@@@######')
        print(result)
        return JsonResponse(result)


# 微博地址发送前端

def weibo_log_view(request):
    if request.method == 'GET':
        data = request.body
        print(data)
        url = get_weibo_login_url()
        return JsonResponse({'code': 200, 'auth_url': url})


def email_active(request):
    if request.method != 'GET':
        result = {'code': 10210, 'message': 'please use GET method'}
        return JsonResponse(result)

    code = request.GET.get('code')
    print(code)
    if not code:
        result = {'code': 10201, 'message': '你的code是错的'}
        return JsonResponse(result)
    try:
        email_code = base64.urlsafe_b64decode(code.encode())
        new_code = email_code.decode()
        username, rcode = new_code.split('_')

    except Exception as e:
        print(e)
        result = {'code': 10201, 'message': '你的email_code是错误的'}
        return JsonResponse(result)

    redis_code= r.get('email_code%s' % username).decode()
    if not redis_code:
        result = {'code': 10201, 'message': '你的redis code是错的'}
        return JsonResponse(result)
    if code != redis_code:
        result = {'code': 10201, 'message': '你的redis中没有code'}
        return JsonResponse(result)
    try:
        user = UserRegist.objects.get(username=username)
        print(user.username,user.isActive)
    except Exception as e:
        result = {'code': 10200, 'message': '获取用户信息错误'}
        return JsonResponse(result)
    user.isActive = True
    user.save()
    result = {'code': 200, 'message': '激活成功'}
    return JsonResponse(result)


# 微博授权处理
def weibo_regist_grant(request):
    if request.method == "GET":
        # 从地址栏中获取到前端请求来的code
        code = request.GET.get('code')

        #     用code向微博服务器发送请求 换取access_token
        try:
            access_token = get_access_token(code)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 10206, 'message': '微博服务器繁忙'})

        """
        微博发送的access_token数据	{access_token:"2.00uF2KpF0VuSON6966e9bef157Uq4D" , remind_in	"157679999" ,
        expires_in	157679999 , uid	"5336721666" , isRealName	"true"}
        """

        # return JsonResponse({'code':200,'access_token':access_token})
        # 判断用户是否时第一次登录
        token = access_token.get('access_token')
        wuid = access_token.get('uid')
        try:
            weibo_user = WeiboUser.objects.get(wuid=wuid)
        except Exception as  e:
            # 用户是第一次登录
            print('用户获取错误，该用户没有登录过')
            WeiboUser.objects.create(wuid=wuid, access_token=token)
            result = {'code': 201, 'uid': wuid}
            return JsonResponse(result)

            # 否则用户不是第一次登录
        else:
            # 用户以前登录过
            # 检查以前有没有绑定过
            # 微博用户外键一对一绑定 注册用户 所以 可以直接点语法查找有没有用户
            users = weibo_user.uid
            print(users)

            if users:
                # 以前登录过绑定过
                # 正常签发token
                token = make_token(users.username)
                print(token)
                result = {'code': 200, 'username': users.username, 'data': token.decode()}
                return JsonResponse(result)
            else:
                # 之前微博登陆过，但是没有执行微博绑定注册
                data = {'code': 201, 'uid': wuid}
                return JsonResponse(data)

    if request.method == "POST":
        pass


def weibo_bind(request):
    if request.method == 'GET':
        return render(request, '../../ICClub/templates/dyy/../weibo_bind.html')

    # TODO 完成微博绑定注册
    if request.method == "POST":
        data = request.body
        js_data = json.loads(data)
        uid = js_data.get('uid')
        print(uid)
        if not uid:
            result = {'code': 10206, 'message': {'error': '服务器繁忙 请稍等'}}
            return JsonResponse(result)

        if not js_data:
            result = {'code': 10200, 'message': {'error': '请完善信息'}}
            return JsonResponse(result)

        username = js_data.get('username')
        if not username:
            return JsonResponse({'code': 10200, 'message': {'error': 'username is not null  '}})

        password = js_data.get('password')
        if not password:
            return JsonResponse({'code': 10200, 'message': {'error': 'password is not null'}})
        print(password)

        passwords = js_data.get('passwords')
        if not passwords:
            return JsonResponse({'code': 10200, 'message': {'error': 'passwords is not null'}})
        print(passwords)

        email = js_data.get('email')
        if not email:
            return JsonResponse({'code': 10200, 'message': {'error': 'email is not null'}})
        print(email)

        phone = js_data.get('phone')
        if not phone:
            return JsonResponse({'code': 10200, 'message': {'error': 'phone is not null '}})
        elif type(phone) != int and len(phone) != 11:
            return JsonResponse({'code': 10200, 'message': {'error': '电话格式错误 '}})
        print(phone)

        code = js_data.get('code')
        if not code:
            return JsonResponse({'code': 10200, 'message': {'error': 'code is not null'}})
        elif len(code) != 6:

            return JsonResponse({'code': 10200, 'message': {'error': '验证码错误 请核对长度'}})

        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()
        print(password)

        ms = hashlib.md5()
        ms.update(passwords.encode())
        passwords = ms.hexdigest()
        print(passwords)
        if passwords != password:
            result = {'code': 10200, 'message': {'error': '密码不一致，请重新输入'}}
            return JsonResponse(result)

        try:
            with transaction.atomic():
                user = UserRegist.objects.create(username=username, password=password, phone=phone, email=email,
                                                 code=code)
                print(user)

                # 用前端传过来的 uid 进行匹配
                weibo_user = WeiboUser.objects.get(wuid=uid)
                print()
                #     关联用户表
                weibo_user.uid = user
                print(weibo_user)

                user.save()

        except Exception as  e:
            # 用户创建不成功  返回错误信息
            print(e)
            result = {'code': 10207, 'message': {'error': 'user is existed'}}
            return JsonResponse(result)

        # 签发token
        token = make_token(username)
        print(token)
        result = {'code': '200', 'username': username, 'token': token.decode()}
        return JsonResponse(result)




# 定义生成token令牌的函数
def make_token(username, exp=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': username, 'exp': exp + now}
    return jwt.encode(payload=payload, key=key, algorithm='HS256')




# 邮箱验证函数
def email_check(s):
    a = re.findall(r'^[a-z0-9A-Z]{1,10}@[0-9a-z]\.{2,4}com|cn', s)
    if a == None:
        return False
    return True





# 前端请求的微博授权地址
def get_weibo_login_url():
    # response_type - code  代表启用授权码模式
    # scope 授权范围
    params = {'response_type': 'code', 'client_id': settings.WEIBO_CLIENT_ID,
              'redirect_uri': settings.WEIBO_REDIRECT_URI, 'scope': ''}
    weibo_url = 'https://api.weibo.com/oauth2/authorize?'
    url = weibo_url + urlencode(params)
    return url


def get_access_token(code):
    # 向资源授权平台 换取token
    token_url = 'https://api.weibo.com/oauth2/access_token'
    post_data = {
        'client_id': settings.WEIBO_CLIENT_ID,
        'client_secret': settings.WEIBO_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.WEIBO_REDIRECT_URI,
        'code': code
    }
    try:
        # 向微博服务器发送post请求
        res = requests.post(token_url, data=post_data)
    except Exception as e:
        print('--weibo request error ')
        print(e)
        raise
    if res.status_code == 200:
        return json.loads(res.text)
    raise


def haa():
    pass
