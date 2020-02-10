from django.conf.urls import url

from label import views

urlpatterns = [
    # 活动投票 GET
    url(r'^/(?P<id>\d+)$',views.Label.as_view()),
    # 获取活动标签 POST
    url(r'^$',views.Label.as_view()),
    url(r'^/option$',views.option),
    url(r'^/hot$',views.LabelHotView.as_view()),

    url(r'^/(\w+)$',views.LabelLikeView.as_view()),
]