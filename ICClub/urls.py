"""ICClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from ICClub import views

urlpatterns = [
    url(r'admin', admin.site.urls),
    # http//127.0.0.1:8000/index
    url(r'^index$', views.index, name='index'),
    url(r'^cir$', views.circle),
    
    # 首页活跃达人栏Ajax测试
    url(r'^v1/activitys/', include('activitys.urls')),
    # 活动评论comment,公告文章评论comment
    url(r'v1/comment/', include('comment.urls')),
    # 登录注册地址
    url(r'^user/', include('users.urls')),
    # 保 测试地址
    url(r'^users/', include('users.urls')),
    # 活动
    url('^active/', include('activitys.urls')),
    url(r'^label', include('activitys.urls')),
    
    # 论坛
    url(r'community', include('community.urls')),
]
