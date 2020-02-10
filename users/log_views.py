import hashlib
import json
import random
import re

import redis
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.baseconv import base64
from django.views.generic.base import View

from users.models import UserRegist
from users.views_regist import make_token
from celery_tasks.user_celery import *

"""
整体思路  用户请求登录 
前端发送数据  
收到数据后  验证用户名密码是否正确

"""

r = redis.Redis(host='localhost',port=6379,db=3)

def login_view(request):
    # if request.method == 'GET':
    #     return render(request, '../templates/dyy/../login.html')

    if request.method == 'POST':

        # print(request.META.get('HTTP_AUTHORIZATION'))
        # 取出前端发送的json对象
        data = request.body

        js_data = json.loads(data)

        if not js_data:
            result = {'code': 10200, 'message': '登录信息不能为空'}
            return JsonResponse(result)
        username = js_data.get('username')
        password = js_data.get('password')
        phone = js_data.get('phone')
        user_code = js_data.get('code')


        if not username and not password and not user_code and not phone:
            result = {'code': 10200, 'message': '登录信息不能为空'}
            return JsonResponse(result)
        # if len(user_code) != 6:
        #     result = {'code': 10202, 'message': '验证码有误'}
        #     return JsonResponse(result)

        # try:
        #     # 取出code核对
        #     redis_code = r.hget(username,phone)
        #     redis_code = json.loads(redis_code)
        # except Exception as e:
        #     print(e)
        #     result = {'code': 10223, 'message': 'redis没有该用户'}
        #     return JsonResponse(result)
        # if user_code != redis_code:
        #     result = {'code': 10224, 'message': '验证码错误,'}
        #     return JsonResponse(result)
        # # 验证完成删除
        # r.hdel(username,phone)

        user = UserRegist.objects.filter(username=username)

        print(user)

        # 用户名是否存在
        if not user:
            result = {'code': 10202, 'message': '用户不存在,点击注册'}
            return JsonResponse(result)

        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()

        # 用户密码是否一致
        users = user[0]
        if password != users.password:
            result = {'code': 10202, 'message': 'username or password is wrong'}
            return JsonResponse(result)

        print(users.id)
        # 签发token
        token = make_token(username)
        # 生成的token为字节串  需要转换为字符串
        result = {'code': 200, 'username': username, 'id': users.id, 'token': token.decode()}
        return JsonResponse(result)


class Find_passwd(View):
    """
    思路 如果是get请求  获取邮箱，验证以前是否注册过，如果是发送邮箱修改密码地址，否 则返回注册
        post请求  验证code是否正确 如正确数据库查询信息，返回200
    """
    def get(self,request):

        email = request.get('email'),
        if not email and isEmail(email) == 0:
            return JsonResponse({'code':'10224','message':'请核对邮箱信息'})
        try:
            user = UserRegist.objects.get(email=email)

        except Exception as e:
            return JsonResponse({'code':10225,'message':'您还没注册过，请先注册'})
        # 信息通过 携带后期验证的加密code发送邮箱链接
        random_num = random.randint(6)
        code_bs = 'pass'+'_'+str(random_num)
        base_code = base64.urlsafe_b64encode(code_bs.encode()).decode('utf-8')
        code_url = 'http://176.209.104.17:7001/templates/find_passwd.html?code=%s' % base_code
        email = user.email
        r.set(email,base_code)
        find_passwd_email.delay(email,code_url)
        return JsonResponse({'code':200,'message':'邮箱已发送'})


    def post(self,request):
        data = request.body
        js_data = json.loads(data)
        email = js_data.get('email')
        code = js_data.get('code')
        username = js_data.get('username')
        phone = js_data.get('username')
        passwd = js_data.get('passwd')
        passwds = js_data.get('passwds')
        if not email and isEmail(email) == 0 and not code:
            return JsonResponse({'code':10224,'message':'邮箱格式有'})

        try:
            code = r.get(email)
            user = UserRegist.objects.get(email=email)
        except Exception as e:
            return JsonResponse({'code':10225,'message':'用户信息错误'})

        redis_code = r.get(email)
        if redis_code != code:
            return JsonResponse({'code':10225,'message':'验证失败'})
        # 验证通过删除redis数据 ,删除mysql密码数据,插入新的数据
        r.delete(email)
        user.delete(passwd)

        m = hashlib.md5()
        m.update(passwd.encode())
        password = m.hexdigest()

        ms = hashlib.md5()
        ms.update(passwds.encode())
        passwords = ms.hexdigest()

        if passwords != password:
            result = {'code': 10200, 'message': '两次密码不一致'}
            return JsonResponse(result)
        # 创建数据
        user.username = username
        user.phone = phone
        user.password = password
        user.isActive = '1'
        user.email = email
        user.save()
        return JsonResponse({'code':200,'message':'修改成功'})




# 邮箱验证正则
def isEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
    