import json
import random
from django.http import JsonResponse
from django.views import View
from celery_tasks.user_celery import send_msm
from django_redis import get_redis_connection

redis_obj = get_redis_connection('user')


class SendSms(View):
	def post(self, request):
		"""
		需要前端传来电话号码，生成验证码  存入redis   后期验证
		"""
		data = request.body
		data = json.loads(data)
		phone_number = str(data.get('phone_number'))
		username = data.get('username')
		if not phone_number and not username:
			result = {'code': 10234, 'message': '参数缺失'}
			return JsonResponse(result)
		code = str(generate_sex_number())
		# 存入redis  等待验证
		redis_obj.hset(username, phone_number, code)
		# 异步发送的短信
		res_code = send_msm(code=code, phone_number=phone_number)
		result = {'message': res_code}
		return JsonResponse(result)


# 随机生成六位验证码
def generate_sex_number(len=6):
	code_list = [str(i) for i in range(10)]
	code = random.sample(code_list, len)
	code = ''.join(code)  # 将列表转为字符串
	return code
