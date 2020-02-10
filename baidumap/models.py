from django.db import models

# Create your models here.

# _*_ encoding:utf-8 _*_
# from __future__ import unicode_literals

from django.db import models


# Create your models here.
class address_info(models.Model):
    # address_longitude为若干个坐标的经度
    longitude = models.FloatField(default=104.06, verbose_name='地图经度')
    # address_latitude为若干个坐标的纬度
    latitude = models.FloatField(default=30.69, verbose_name='地图纬度')
    # address_data为标记上所需要显示的数据
    data = models.CharField(default=None,max_length=200)
