from django.conf.urls import url

from users import views, log_views, views_regist, sendsms_views

urlpatterns = [
    url(r'^home$', views.user_info),
    url(r'^update$', views.update_user_info),
    # 上传图片测试
    url(r'^upload$', views.upload_img),
    # url(r'^$', views.Users.as_view()),
     # 登录地址
    url(r'^login$', log_views.login_view, ),
    # 注册地址
    url(r'^regist$', views_regist.regist_view, name='regist'),
    #     前端获取微博登录地址
    url(r'^weibo$', views_regist.weibo_log_view, name='weibo_log'),
    #   微博回调地址
    url(r'^grant$', views_regist.weibo_regist_grant, name='weibo_grant'),
    #   微博授权注册地址
    url(r'^bind', views_regist.weibo_bind, name='weibo_bind'),
    # 邮箱激活账户
    url(r'email_activ', views_regist.email_active),
    # 短信发送
    url(r'send_sms', sendsms_views.SendSms.as_view()),
    url(r'find_passwd', log_views.Find_passwd.as_view()),
]
