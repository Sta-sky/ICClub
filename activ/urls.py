from django.conf.urls import url
from . import views, test_search

urlpatterns = [

    url(r'^create$', views.Active.as_view()),
    url(r'^new/(\d+)$', views.get_new),
    url(r'^history/(\d+)$', views.hyistorical_activities),


    url(r'^index/hot$', views.ActIndexView.as_view()),

    #http://127.0.0.1:8000/activ/search/1
    url(r'^search/(\d+)$', views.activitySearchView),

    url(r'^detail$', views.ActivityDetailView.as_view()),

    # http://127.0.0.1:8000/v1/activ/actvuser1
    url(r'^actvuser$', views.active_users),

    # http://127.0.0.1:8000/v1/activ/actvuser2
    url(r'^actvuser2$', views.get_active_users),
    # 127.0.0.1:8000/v1/activ/article
    url(r'^article$', views.get_admin_articles),
    # 127.0.0.1:8000/v1/activ/article_info?...
    url(r'^article_info$', views.article_info),
]
