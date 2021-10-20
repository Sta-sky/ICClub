import base64
import json
import random
import re
import jwt
import time
import requests
from ICClub import settings
#   事务
from tools.util import decode_md5, verify_sms_code
from django.db import transaction
from urllib.parse import urlencode
from django.shortcuts import render
from tools.response_code import code
from activitys.models import UserInfo
from django.http import  JsonResponse
from django_redis import get_redis_connection
from users.models import UserRegist, WeiboUser
from celery_tasks.user_celery import send_act_email

redis_obj = get_redis_connection('user')


# 网站用户注册
def regist_view(request):
    if request.method == "GET":
        return render(request, '../templates/dyy/../regist.html')

    if request.method == 'POST':
        # 前端使用了stringify  转换成了json的字符串 所以  需要loads（）一下  转换成json对象
        data = request.body
        # 将json字符串转换成为 接送对象
        json_data = json.loads(data)
        if not json_data:
            return JsonResponse(code[10209])
        # TODO  邮箱正则
        username = json_data.get('username')
        password = json_data.get('password')
        passwords = json_data.get('passwords')
        email = json_data.get('email')
        phone = json_data.get('phone')
        user_code = json_data.get('code')
        if not username or not password or not passwords or not phone or not user_code:
            code[10208]['message'] = '注册信息不完整'
            return JsonResponse(code[10208])
        if not email_check(email):
            code[10208]['message'] = '邮箱格式错误'
            return JsonResponse(code[10208])
    
        # TODO 此处加手机验证码 判断
        # verify_result = verify_sms_code(redis_obj, username, phone, user_code)
        # if verify_result:
        #     return verify_result
        # 判断两次密码是否一致
        passwd_one = decode_md5(password)
        passwd_tow = decode_md5(passwords)
        if passwd_one != passwd_tow:
            code[10208]['message'] = '两次密码不一致'
            return JsonResponse(code[10208])
        # 从数据库中过滤  是否已经有了前端传来的username
        user = UserRegist.objects.filter(username=username)
        if user:
            code[10208]['message'] = '用户名已经存在,请换个昵称试试'
            return JsonResponse(code[10208])
        try:
            user = UserRegist.objects.create(username=username, password=passwd_one, email=email,
                                             phone=phone, code=user_code)
            UserInfo.objects.create(nickname=username, user_id=user.id)
        except Exception as e:
            code[10208]['message'] = '插入用户数据失败'
            return JsonResponse(code[10208])
        # 签发token
        token = make_token(username)
        # TODO 激活邮件
        random_num = random.randint(1000, 9999)
        code_random = username + '_' + str(random_num)
        base_code = base64.urlsafe_b64encode(code_random.encode()).decode('utf-8')
        # 将数据存入缓存中  等待用户发送请求验证  激活
        redis_obj.set('email_code%s' % username, base_code)
        email_url = settings.EMAIL_URL.format(base_code)
        try:
            send_act_email.delay(email, email_url)
        except Exception as e:
            code[10208]['message'] = f'邮箱发送失败 !请核对邮箱, {e}'
            return JsonResponse(code[10208])
        result = {'code': 200, 'username': username, 'id': user.id, 'token': token.decode()}
        return JsonResponse(result)


# 微博地址发送前端
def weibo_log_view(request):
    if request.method == 'GET':
        data = request.body
        url = get_weibo_login_url()
        return JsonResponse({'code': 200, 'auth_url': url})


def email_active(request):
    if request.method != 'GET':
        return JsonResponse(code[10506])
    code_email = request.GET.get('code')
    try:
        email_code = base64.urlsafe_b64decode(code_email.encode())
        new_code = email_code.decode()
        username, rcode = new_code.split('_')
    except Exception as e:
        code[10208]['message'] = '你的验证码是错的'
        return JsonResponse(code[10208])
    redis_code= redis_obj.get('email_code%s' % username).decode()
    if not redis_code:
        code[10208]['message'] = 'redis获取验证码服务异常'
        return JsonResponse(code[10208])
    if code_email != redis_code:
        code[10208]['message'] = '验证码错误用户激活失败'
        return JsonResponse(code[10208])
    try:
        user = UserRegist.objects.get(username=username)
        print(user.username,user.isActive)
    except Exception as e:
        return JsonResponse(code[10210])
    user.isActive = True
    user.save()
    code[200]['message'] = '激活成功'
    return JsonResponse(code[200])


# 微博授权处理
def weibo_regist_grant(request):
    if request.method == "GET":
        # 从地址栏中获取到前端请求来的code
        verify_code = request.GET.get('code')
        # 用code向微博服务器发送请求 换取access_token
        try:
            access_token = get_access_token(verify_code)
        except Exception as e:
            code[10208]['message'] = f'微博服务器繁忙，原因为{e}'
            return JsonResponse(code[10208])
        """
        微博发送的access_token数据	{access_token:"2.00uF2KpF0VuSON6966e9bef157Uq4D" , remind_in	"157679999" ,
        expires_in	157679999 , uid	"5336721666" , isRealName	"true"}
        """
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
        else:
            # 用户以前登录过 检查以前有没有绑定过
            # 微博用户外键一对一绑定 注册用户 所以 可以直接点语法查找有没有用户
            users = weibo_user.uid
            if users:
                # 以前登录过绑定过 正常签发token
                token = make_token(users.username)
                print(token)
                result = {'code': 200, 'username': users.username, 'data': token.decode()}
                return JsonResponse(result)
            else:
                # 之前微博登陆过，但是没有执行微博绑定注册
                data = {'code': 201, 'uid': wuid}
                return JsonResponse(data)
    if request.method == "POST":
        return JsonResponse(code[10506])


def weibo_bind(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    # TODO 完成微博绑定注册
    if request.method == "POST":
        data = request.body
        js_data = json.loads(data)
        uid = js_data.get('uid')
        if not uid:
            return JsonResponse(code[10209])
        info_dic = {}
        info_dic['username'] = js_data.get('username')
        info_dic['passwd_one'] = js_data.get('password')
        info_dic['passwd_tow'] = js_data.get('passwords')
        info_dic['email'] = js_data.get('email')
        info_dic['phone'] = js_data.get('phone')
        info_dic['code_sms'] = js_data.get('code')
        for key, val in info_dic.items():
            if not key:
                code[10208]['message'] = f'传入的 {key} 信息为空'
                return JsonResponse(code[10208])
            if key == 'phone' and type(key) != int or len(key) != 11:
                code[10208]['message'] = '电话格式错误'
                return JsonResponse(code[10208])
            if key == 'code_sms' and type(key) != int or len(key) != 11:
                code[10208]['message'] = '验证码为空'
                return JsonResponse(code[10208])
                
        passwd_one = decode_md5(info_dic['passwd_one'])
        passwd_tow = decode_md5(info_dic['passwd_tow'])
        
        if passwd_one != passwd_tow:
            code[10208]['message'] = '密码不一致，请重新输入'
            return JsonResponse(code[10208])
        try:
            with transaction.atomic():
                user = UserRegist.objects.create(
                    username=info_dic['username'], password=info_dic['passwd_one'],
                    phone=info_dic['phone'], email=info_dic['email'], code=info_dic['code_sms'])
                # 用前端传过来的 uid 进行匹配
                weibo_user = WeiboUser.objects.get(wuid=uid)
                # 关联用户表
                weibo_user.uid = user
                user.save()
        except Exception as  e:
            # 用户创建不成功  返回错误信息
            return JsonResponse(code[10211])
        # 签发token
        token = make_token(info_dic['username'])
        print(token)
        result = {'code': '200', 'username': info_dic['username'], 'token': token.decode()}
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
