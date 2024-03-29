# Generated by Django 3.2.7 on 2021-10-08 13:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='活动主题')),
                ('content', models.TextField(verbose_name='活动内容')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击量')),
                ('act_img', models.ImageField(default=None, upload_to='images/activity/', verbose_name='活动图片')),
                ('beg_time', models.DateTimeField(default=datetime.date.today, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(null=True, verbose_name='结束时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.SmallIntegerField(choices=[(1, '活动发起中'), (2, '活动中'), (3, '活动结束')], verbose_name='活动状态')),
                ('version', models.IntegerField(default=0, verbose_name='库存版本')),
                ('is_visiable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('condition', models.SmallIntegerField(default=10, verbose_name='活动人数条件')),
                ('active_address', models.CharField(default=None, max_length=100, verbose_name='活动地点')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏数')),
            ],
            options={
                'verbose_name_plural': '活动创建表',
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='address_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField(default=104.06, verbose_name='地图经度')),
                ('latitude', models.FloatField(default=30.69, verbose_name='地图纬度')),
                ('data', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InterestTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interests', models.CharField(max_length=100, unique=True, verbose_name='爱好标签')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('img_url', models.ImageField(null=True, upload_to='images/label/', verbose_name='默认图片')),
            ],
            options={
                'verbose_name_plural': '兴趣标签',
                'db_table': 'interest_tag',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30, unique=True, verbose_name='昵称')),
                ('gender', models.CharField(default='男', max_length=10, verbose_name='性别')),
                ('birth', models.DateTimeField(null=True, verbose_name='出生年月')),
                ('city', models.CharField(max_length=100, null=True, verbose_name='常住城市')),
                ('introduction', models.TextField(null=True, verbose_name='个人描述')),
                ('portrait', models.ImageField(default='images/user_head/boy1.jpg', upload_to='images/user_head/', verbose_name='头像路径')),
                ('credit', models.IntegerField(default=100, verbose_name='信誉积分')),
                ('level', models.IntegerField(default=0, verbose_name='账号等级')),
                ('login_days', models.IntegerField(default=0, verbose_name='登录天数')),
                ('sponsor_num', models.IntegerField(default=0, verbose_name='发起活动数')),
                ('participate_num', models.IntegerField(default=0, verbose_name='参与活动数')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('interest', models.ManyToManyField(default=None, to='activitys.InterestTag', verbose_name='爱好标签')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userregist', verbose_name='注册信息id')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='AdminArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='活动主题')),
                ('content', models.TextField(verbose_name='活动内容')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击量')),
                ('act_img', models.ImageField(default=None, upload_to='images/official/', verbose_name='活动图片')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_visiable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏数')),
                ('tag_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='activitys.interesttag', verbose_name='活动标签')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userregist', verbose_name='发起人')),
            ],
            options={
                'verbose_name_plural': '管理员文章',
                'db_table': 'admin_article',
            },
        ),
        migrations.CreateModel(
            name='ActivityParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='activitys.activity', verbose_name='活动')),
                ('user', models.ManyToManyField(default=None, to='activitys.UserInfo', verbose_name='参与者')),
            ],
            options={
                'verbose_name_plural': '活动参与表',
                'db_table': 'activity_participant',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activitys.interesttag', verbose_name='活动标签'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userregist', verbose_name='发起人'),
        ),
    ]
