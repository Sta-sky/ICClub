from django.conf.urls import url

from comment import views, tests

urlpatterns = [
    # http://127.0.0.1:8000/v1/comment/act?actid=xx&uid=xx
    url(r'act',views.ActivityCommentView.as_view()),
    # http://127.0.0.1:8000/v1/comment/article?articleid=xx&uid=xx
    url(r'art',views.ArticleCommentView.as_view()),
    # 测试
    # http://127.0.0.1:8000/v1/comment/act?actid=xx&uid=xx
    # url(r'act', tests.ActivityCommentView.as_view()),
]
