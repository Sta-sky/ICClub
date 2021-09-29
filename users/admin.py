from django.contrib import admin

# Register your models here.
from users.models import UserRegist, WeiboUser

print('============')
class UserRegist_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'username', 'email', 'phone', 'isActive', 'create_time', 'update_time']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['username']
    # 指定列表页右侧的过滤器
    # list_filter = ['pub']
    # 指定列表页左上方的搜索栏
    # search_fields = ['title', 'market_price']
    # 指定列表页可修改的字段值
    # list_editable = ['price']


class WeiboUser_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['uid', 'wuid', 'access_token']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['wuid']


# 导入想在admin后台管理的数据类
admin.site.register(UserRegist, UserRegist_Manager)
admin.site.register(WeiboUser, WeiboUser_Manager)
