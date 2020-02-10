import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# import base64

# 上传图片测试
def test(request):
    return HttpResponse('你好')
    # print(request.method)
    # if request.method == 'POST':
    #     json_data = request.body
    #     data = json.loads(json_data)
    #     file = data.get('data').split(',')[1]
    #     file = base64.b64decode(file)
    #
    #     with open('/home/tarena/桌面/123.jpg', 'wb') as f:
    #         f.write(file)
    #
    #     # print(file_obj)  # file_obj就是文件对象
    #     # 文件名
    #     # 文件操作 将上传的文件写入后端
    #
    #     return JsonResponse({'code': 200, 'message': '收到'})
    # return JsonResponse({'code': 200, 'message': '??????????'})


# def test(request):
#
#     return HttpResponse('你好')

def index(request):
    return render(request, 'lxj/templates/activity.html')


def circle(request):
    data = '参加这个活动，收获很多参加这个活动，收获很多'
    return render(request, 'test_circle.html', locals())

# def error404_page(request):
#     return render(request, 'wz/notfound.html')
