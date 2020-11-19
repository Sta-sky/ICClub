from django.shortcuts import render


def index(request):
    return render(request, 'lxj/templates/activitys.html')


def circle(request):
    data = '参加这个活动，收获很多参加这个活动，收获很多'
    return render(request, 'test_circle.html', locals())

