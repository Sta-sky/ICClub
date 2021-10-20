from django.conf.urls import url

from community import views

urlpatterns = {
	url('index', views.community_index),
	url('hot_commnet', views.hot_commnet),
	url('like_commnet', views.like_commnet),
	url('search_hot', views.search_hot),
}