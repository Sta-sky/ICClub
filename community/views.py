from django.http import JsonResponse
from tools.response_code import code
from .models import Article
from dwebsocket.decorators import accept_websocket
from django.core.paginator import Paginator

def community_index(request):
	if request.is_websockte():
		currnet_page = request.GET.get('page')
		print(currnet_page)
		try:
			community_obj = Article.objects.filter.all().order_by('create_time')[:80]
			page_obj = Paginator(community_obj, 8)
			# 总页数
			totle_page_num = page_obj.num_pages
			res_data = param_community_data(community_obj, page_obj)
			result = {'code': 200, 'data': res_data, 'page': {'currnet_page': currnet_page, 'totle_page': totle_page_num}}
			return JsonResponse(result)
		except Exception as e:
			return JsonResponse(code[10507])
		

def hot_commnet(request):
	
	pass

def like_commnet(request):
	pass

def search_hot(request):
	pass


def param_community_data(comm_obj, page_obj):
	comm_data_list = []
	try:
		if comm_obj and page_obj:
			for comm in page_obj.object_list:
				comm_data_dic = {
				    'commnuity_user': comm.commnuity_user.username,
				    'lable': comm.lable.lable_name,
				    'commnuit_content': comm.commnuit_content,
				    'create_time': comm.create_time,
				    'click_num': comm.click_num,
				    'commnuit_img': comm.commnuit_img,
				}
				comm_data_list.append(comm_data_dic)
	except Exception as e:
		code[10508]['message'] = e
		return JsonResponse(code[10508])
	return comm_data_list