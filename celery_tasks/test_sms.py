import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.mail import send_mail
from celery_tasks.task import app

class AliSendSms():
    def __init__(self):
        self.AccessKeyID = 'LTAI4FkMsLNq5z6dkiUGbZXA'
        self.AccessKeySecret = 'LGOV2fHv52iQILNKMIk6gmDO4Sz8xg'
        self.SignName = "ICClub"
        self.TemplatesCode = "SMS_180355434"

    def generate_request(self, code, phone_number):
        request = CommonRequest()
        # 默认为json格式
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        # 默认为post请求
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "default")
        request.add_query_param('PhoneNumbers', phone_number)
        request.add_query_param('SignName', self.SignName)
        request.add_query_param('TemplateCode', self.TemplatesCode)
        request.add_query_param('TemplateParam', "{'code':" + code + '}')

        return request


    # 生成客户端的请求，
    def generate_client(self):
        clint = AcsClient(self.AccessKeyID, self.AccessKeySecret, 'default')
        return clint


    def send_msm(self, code, phone_number):
        client = self.generate_client()
        request = self.generate_request(code ,phone_number)

        try:
            response = client.do_action_with_exception(request)  # 字节串类型
            response = response.decode()  # 字符串

            response_dict = json.loads(response)  # json对象
            print(response_dict['message'])
            result = response_dict['Code']
            return result
        except Exception as e:
            print('获取验证码错误')



a = AliSendSms()
phone = '18419360851'
code = str(122321)
print(a.send_msm(code,phone))