from datetime import date
from django.conf import settings
from django.db import models
from users.models import UserRegist

ACTIVITY_STATUS = (
    (1, '活动发起中'),
    (2, '活动中'),
    (3, '活动结束'),
)

class InterestTag(models.Model):
    # 兴趣标签表
    interests = models.CharField(max_length=100, verbose_name='爱好标签', unique=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    img_url = models.ImageField(upload_to=settings.DBLABIMG, verbose_name='默认图片', null=True)

    class Meta:
        db_table = 'interest_tag'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '兴趣标签'

    def __str__(self):
        return 'id:%s nickname:%s' % (self.id, self.interests)
    

class UserInfo(models.Model):
    # 用户信息表
    nickname = models.CharField(max_length=30, verbose_name='昵称', unique=True)
    gender = models.CharField(max_length=10, verbose_name='性别', default='男')
    birth = models.DateTimeField(verbose_name='出生年月', null=True)
    city = models.CharField(max_length=100, verbose_name='常住城市', null=True)
    introduction = models.TextField(verbose_name='个人描述', null=True)
    portrait = models.ImageField(upload_to=settings.DBUSEIMG, default='images/user_head/boy1.jpg', verbose_name='头像路径')
    credit = models.IntegerField(default=100, verbose_name='信誉积分')
    level = models.IntegerField(default=0, verbose_name='账号等级')
    login_days = models.IntegerField(default=0, verbose_name='登录天数')
    # 发起活动数
    sponsor_num = models.IntegerField(default=0, verbose_name='发起活动数')
    # 参与活动数
    participate_num = models.IntegerField(default=0, verbose_name='参与活动数')
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    user = models.OneToOneField(UserRegist, verbose_name='注册信息id')
    interest = models.ManyToManyField(InterestTag, verbose_name='爱好标签', default=None)

    class Meta:
        db_table = 'user_info'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '用户信息'

    def __str__(self):
        return 'id:%s nickname:%s' % (self.id, self.nickname)


class Activity(models.Model):
    # 活动创建表
    user = models.ForeignKey(UserRegist, verbose_name='发起人')
    tag = models.ForeignKey(InterestTag, verbose_name='活动标签')
    subject = models.CharField(max_length=100, verbose_name='活动主题')
    content = models.TextField(verbose_name='活动内容')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    act_img = models.ImageField(upload_to=settings.DBACTIMG,verbose_name='活动图片', default=None)
    beg_time = models.DateTimeField(verbose_name='开始时间', null=False, default=date.today)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    status = models.SmallIntegerField(verbose_name='活动状态', choices=ACTIVITY_STATUS)
    version = models.IntegerField(default=0, verbose_name="库存版本")
    is_visiable = models.BooleanField(default=True, verbose_name='是否可见')
    condition = models.SmallIntegerField(verbose_name='活动人数条件', default=10)
    activ_address = models.CharField(max_length=100, verbose_name='活动地点', default=None)
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    collection = models.IntegerField(default=0, verbose_name='收藏数')

    class Meta:
        db_table = 'activity'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '活动创建表'

    def __str__(self):
        return 'id:%s activity_subject:%s' % (self.id, self.subject)


# 官方活动创建表 官方 官方
class AdminArticle(models.Model):
    user = models.ForeignKey(UserRegist, verbose_name='发起人')
    tag_id = models.ForeignKey(InterestTag, verbose_name='活动标签', default=None)
    subject = models.CharField(max_length=100, verbose_name='活动主题')
    content = models.TextField(verbose_name='活动内容')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    act_img = models.ImageField(upload_to=settings.DBOFFIMG,verbose_name='活动图片', default=None)
    # TODO 下面两个刚添加的字段 如报错可以注释
    # beg_time = models.DateTimeField(verbose_name='开始时间', null=False, default=date.today)
    # end_time = models.DateTimeField(verbose_name='结束时间', null=True)

    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    # status = models.SmallIntegerField(verbose_name='活动状态', choices=ACTIVITY_STATUS)
    is_visiable = models.BooleanField(default=True, verbose_name='是否可见')

    likes = models.IntegerField(default=0, verbose_name='点赞数')
    collection = models.IntegerField(default=0, verbose_name='收藏数')

    class Meta:
        db_table = 'admin_article'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '管理员文章'

    def __str__(self):
        return 'id:%s activity_subject:%s' % (self.id, self.subject)


class ActivityParticipant(models.Model):
    # 活动参与者表
    user = models.ManyToManyField(UserInfo, verbose_name='参与者', default=None)
    activity = models.OneToOneField(Activity, verbose_name='活动')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'activity_participant'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '活动参与表'

    def __str__(self):
        return 'user:%s activity_subject:%s' % (self.user, self.activity)


class address_info(models.Model):
    # address_longitude为若干个坐标的经度
    longitude = models.FloatField(default=104.06, verbose_name='地图经度')
    # address_latitude为若干个坐标的纬度
    latitude = models.FloatField(default=30.69, verbose_name='地图纬度')
    # address_data为标记上所需要显示的数据
    data = models.CharField(default=None,max_length=200)
    
