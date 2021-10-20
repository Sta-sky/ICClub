import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.mail import send_mail
from celery_tasks.task import app

@app.task()
def send_act_email(email, code_url):
    subject = 'ICClub用户激活邮件'
    html_message = '<p>尊敬的用户 您好</p>' \
                   '<p>ICClub激活地址为<a href="' + code_url + '" target="blank">请点击激活</a></p>'
    print(html_message)
    print(b'wolaile'.decode())
    send_mail(subject, '', '1361704733@qq.com', html_message=html_message, recipient_list=[email])

@app.task()
def send_active_mail(email, title, time):
    subject = 'ICClub活动达成通知'
    html_message = """
        <p>尊敬的用户，您好</p>
        <p>您投票的主题活动已创建成功，活动主题为{}，时间：{}，感谢您的参与</p>""".format(title, time)
    send_mail(subject, '', '1361704733@qq.com', html_message=html_message, recipient_list=[email])


# 找回密码
@app.task()
def find_passwd_email(email, code_url):
    subject = 'ICClub用户密码找回邮件'
    html_message = '<p>尊敬的用户 您好</p>' \
                   '<p>ICClub密码找回链接地址为<a href="' + code_url + '" target="blank">请点击激活</a></p>'
    print(html_message)
    send_mail(subject, '', '1361704733@qq.com', html_message=html_message, recipient_list=[email])


"""
# 阿里云短信接口安装包
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  aliyun-python-sdk-core
"""

# 定义短信发送函数
AccessKeyID = 'LTAI4FkMsLNq5z6dkiUGbZXA'  # 密钥id
AccessKeySecret = 'LGOV2fHv52iQILNKMIk6gmDO4Sz8xg'  # 密钥
SignName = "ICClub"  # 注册名称
TemplatesCode = "SMS_180355434"  # 短信模板id


# 生成向阿里云的请求
def generate_request(code, phone_number):
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
    request.add_query_param('SignName', SignName)
    request.add_query_param('TemplateCode', TemplatesCode)
    request.add_query_param('TemplateParam', "{'code':" + code + '}')
    return request


# 生成客户端的请求，
def generate_client():
    return AcsClient(AccessKeyID, AccessKeySecret, 'default')


@app.task()
def send_msm(code, phone_number):
    client = generate_client()
    request = generate_request(code, phone_number)
    response = client.do_action_with_exception(request)  # 字节串类型
    response = response.decode()  # 字符串
    response_dict = json.loads(response)  # json对象

    return response_dict['Code'], response_dict['Message']


