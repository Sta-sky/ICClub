import json

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from requests import request

from .models import address_info


def baidu(request):
    address_point = address_info.objects.all()
    address_longitude = []
    address_latitude = []
    address_data = []
    for i in range(len(address_point)):
        address_longitude.append(address_point[i].longitude)
        address_latitude.append(address_point[i].latitude)
        address_data.append(address_point[i].data)

    return render(request, 'address.html',
                  {'address_longitude': json.dumps(address_longitude),
                   'address_latitude': json.dumps(address_latitude), 'address_data': json.dumps(address_data)})


def iptest(request):
    if request == 'get':
        BAIDU_MAP = 'http://api.map.baidu.com/location/ip?ip=176.209.104.17&ak=&coor=bd09ll'
        return JsonResponse({'code':200})