from django.contrib import admin

# Register your models here.
from activitys.models import UserInfo, InterestTag, Activity, ActivityParticipant, AdminArticle


# class UserRegist_Manager(admin.ModelAdmin):
# 定义列表也显示的字段
# list_display = ['id', 'username']
# 指定哪个字段可以跳转到详情页面
# list_display_links = ['title']
# 指定列表页右侧的过滤器
# list_filter = ['pub']
# 指定列表页左上方的搜索栏
# search_fields = ['title', 'market_price']
# 指定列表页可修改的字段值
# list_editable = ['price']


# 兴趣表
class InterestTag_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'interests', 'created_time', 'updated_time']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['interests']


# 用户信息表
class UserInfo_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'nickname', 'gender', 'birth', 'city', 'introduction', 'portrait', 'credit', 'level',
                    'login_days', 'sponsor_num', 'participate_num', 'likes']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['nickname']


# 活动创建表
class Activity_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'subject', 'click_nums', 'act_img', 'beg_time', 'end_time', 'status', 'version',
                    'created_time', 'updated_time']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['subject']


# 管理员文章表
class AdminArticle_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'subject', 'click_nums', 'act_img', 'created_time', 'updated_time']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['subject']


class ActivityParticipant_Manager(admin.ModelAdmin):
    # 定义列表也显示的字段
    list_display = ['id', 'created_time', 'updated_time']
    # 指定哪个字段可以跳转到详情页面
    list_display_links = ['id']


# 导入想在admin后台管理的数据类
admin.site.register(InterestTag, InterestTag_Manager)
admin.site.register(UserInfo, UserInfo_Manager)
admin.site.register(Activity, Activity_Manager)
admin.site.register(AdminArticle, AdminArticle_Manager)
admin.site.register(ActivityParticipant, ActivityParticipant_Manager)
