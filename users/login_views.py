import re
import random
from ICClub import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.baseconv import base64
from django.views.generic.base import View
from tools.response_code import code
from tools.util import decode_md5, verify_sms_code
from users.models import UserRegist
from users.regist_views import make_token
from celery_tasks.user_celery import *
from django_redis import get_redis_connection
"""
整体思路  用户请求登录 
前端发送数据  
收到数据后  验证用户名密码是否正确
"""

redis_obj = get_redis_connection('user')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        print(request.META.get('HTTP_AUTHORIZATION'))
        # 取出前端发送的json对象
        data = request.body
        js_data = json.loads(data)
        if not js_data:
            code[10209]['message'] = '登录信息不能为空'
            return JsonResponse(code)
        username = js_data.get('username')
        password = js_data.get('password')
        phone = js_data.get('phone')
        user_code = js_data.get('code')
        if not username and not password and not user_code and not phone:
            result = {'code': 10200, 'message': '登录信息不能为空'}
            return JsonResponse(result)
        if len(user_code) != 6:
            result = {'code': 10202, 'message': '验证码有误'}
            return JsonResponse(result)
        # verify_result = verify_sms_code(redis_obj, username, phone, user_code)
        # if verify_result:
        #     return verify_result
        user = UserRegist.objects.filter(username=username)
        # 用户名是否存在
        if not user:
            return JsonResponse(code[10205])
        password = decode_md5(password)
        # 用户密码是否一致
        users = user[0]
        if password != users.password:
            return JsonResponse(code[10212])
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
        if not email or isEmail(email) == 0:
            return JsonResponse(code[10209])
        try:
            user = UserRegist.objects.get(email=email)
        except Exception as e:
            return JsonResponse(code[10213])
        # 信息通过 携带后期验证的加密code发送邮箱链接
        random_num = random.randint(0,9)
        code_bs = 'pass'+'_'+str(random_num)
        base_code = base64.urlsafe_b64encode(code_bs.encode()).decode('utf-8')
        code_url = settings.EMAIL_URL.format(base_code)
        email = user.email
        redis_obj.set(email,base_code)
        find_passwd_email.delay(email, code_url)
        code[200]['message'] = '邮箱已发送'
        return JsonResponse(code[200])

    def post(self,request):
        data = request.body
        js_data = json.loads(data)
        email = js_data.get('email')
        code = js_data.get('code')
        username = js_data.get('username')
        phone = js_data.get('username')
        passwd = js_data.get('passwd')
        passwds = js_data.get('passwds')
        if not email or isEmail(email) == 0 or not code:
            return JsonResponse(code[10209])
        try:
            code = redis_obj.get(email)
            user = UserRegist.objects.get(email=email)
        except Exception as e:
            return JsonResponse(code[10210])
        redis_code = redis_obj.get(email)
        if redis_code != code:
            return JsonResponse(code[10216])
        # 验证通过删除redis数据 ,删除mysql密码数据,插入新的数据
        redis_obj.delete(email)
        user.delete(passwd)
        password = decode_md5(passwd)
        passwords = decode_md5(passwds)
        if passwords != password:
            return JsonResponse(code[10214])
        # 创建数据
        user.username = username
        user.phone = phone
        user.password = password
        user.isActive = '1'
        user.email = email
        user.save()
        code[200]['message'] = '密码修改成功'
        return JsonResponse(code[200])




# 邮箱验证正则
def isEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
    