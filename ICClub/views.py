import os

from django.shortcuts import render


def index(request):
    return render(request, 'activity.html')


def circle(request):
    data = '参加这个活动，收获很多参加这个活动，收获很多'
    return render(request, 'test_circle.html', locals())

