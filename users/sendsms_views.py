import json
import random
from django.http import JsonResponse
from django.views import View

from celery_tasks.user_celery import send_msm
import redis


r = redis.client.Redis(host='localhost',port=6379,db=3)


class SendSms(View):
    def post(self,request):
        print('进来了')
        """
        需要前端传来电话号码，生成验证码
        存入redis   后期验证
        :param request:
        :return:
        """
        data = request.body
        print('##########')

        data = json.loads(data)
        print(data)

        phone_number = str(data.get('phone_number'))
        print(phone_number)
        username = data.get('username')
        print(username)

        if not phone_number and not username:
            result = {'code':10234,'message':'参数缺失'}
            return JsonResponse(result)
        code = str(generate_sex_number())
        print('$#$#$#$#$#$#')
        print(type(code))
        # 存入redis  等待验证
        r.hset(username,phone_number,code)

        # 异步发送的短信
        print(code)
        # try:
        res_code = send_msm(code=code,phone_number=phone_number)
        print('@@@@@@@@@@@@@@@@')
        result = {'message':res_code}
        print(result)
        return JsonResponse(result)


    # def post(self,request):
    #     """
    #     发送信息
    #     :param request:
    #     :return:
    #     """
    #     data = request.body
    #     data = json.loads(data)
    #     if not data :
    #         result = {'code':10222,'message':'没有有效的参数'}
    #         return JsonResponse(result)
    #     phone = data.get('phone')
    #     user_code = data.get('code')
    #     if len(phone) == 0 or len(user_code) == 0:
    #         result = {'code': 10222, 'message': '没有有效的参数'}
    #         return JsonResponse(result)
    #     try:
    #         redis_code = r.hget()
    #     except Exception as e:
    #         print(e)
    #         result = {'code': 10223, 'message': 'rdis数据库繁忙'}
    #         return JsonResponse(result)
    #     if user_code != redis_code:
    #         result = {'code': 10224, 'message': '验证码错误,'}
    #         return JsonResponse(result)
    #     result = {'code':200}
    #     return JsonResponse(result)




# 随机生成六位验证码
def generate_sex_number(len = 6):
    code_list = []
    for i in  range(10):
        code_list.append(str(i))
    # for i in  range(65,91):         #生成A-Z的Ascll编码
    #     code_list.append(chr(i))
    # for i in  range(97,123):        #生成a-z的ascll编码
    #     code_list.append(chr(i))
        # sample从数据集合中拿出指定长度的字符
    code = random.sample(code_list,len)
    code = ''.join(code)            #将列表转为字符串
    return code




