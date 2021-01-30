from django.db import models


# Create your models here.
# 注册表


class UserRegist(models.Model):
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    isActive = models.BooleanField(default=False, verbose_name='是否激活')
    phone = models.BigIntegerField(verbose_name='手机号码')
    code = models.IntegerField(verbose_name='验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_regist'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '注册表'

    def __str__(self):
        return '%s_%s_%s_%s_%s' % (self.username, self.email, self.phone, self.isActive, self.code)


class WeiboUser(models.Model):
    # 微博用户表
    uid = models.OneToOneField(UserRegist, null=True, on_delete=models.CASCADE)
    wuid = models.CharField(max_length=50, db_index=True, verbose_name='微博用户ID')
    access_token = models.CharField(max_length=100, verbose_name='授权令牌')

    class Meta:
        db_table = 'weibo_user'
        # 该对象复数形式的名称(复数), 用于显示在admin管理界面中
        verbose_name_plural = '微博用户表'

    def __str__(self):
        return '%s_%s' % (self.wuid, self.uid)
