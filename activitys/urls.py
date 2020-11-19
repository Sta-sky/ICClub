from django.conf.urls import url
from . import views, lable_views, map_views

urlpatterns = [
    
    # TODO  活动相关
    url(r'^create$', views.Active.as_view()),                       # 创建活动
    url(r'^new/(\d+)$', views.get_new),                             # 最新活动
    url(r'^history/(\d+)$', views.hyistorical_activities),          # 历史活动
    url(r'^index/hot$', views.ActHotIndex.as_view()),              # 最热活动
    url(r'^search/(\d+)$', views.activitySearchView),               # http://127.0.0.1:8000/activ/search/1
    url(r'^detail$', views.ActivityDetailView.as_view()),           # 活动详情
    url(r'^actvuser$', views.active_users),                         # lable页活动达人  http://127.0.0.1:8000/v1/activ/actvuser1
    url(r'^actvuser2$', views.get_active_users),                    # lable页活动达人 http://127.0.0.1:8000/v1/activ/actvuser2
    url(r'^article$', views.get_admin_articles),                    # 管理员活动 http://127.0.0.1:8000/v1/activ/article
    url(r'^article_info$', views.article_info),                     # http://127.0.0.1:8000/v1/activ/article_info?...
    
    # TODO lable_views  start
    # 活动投票 GET
    url(r'^/(?P<id>\d+)$', lable_views.Label.as_view()),
    # 获取活动标签 POST
    url(r'^$', lable_views.Label.as_view()),
    url(r'^/option$', lable_views.option),
    url(r'^/hot$', lable_views.LabelHotView.as_view()),
    url(r'^/(\w+)$', lable_views.LabelLikeView.as_view()),
    
    #TODO 百度地图
    url(r'^com$', map_views.baidu),
]
