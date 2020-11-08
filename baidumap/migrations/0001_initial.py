# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-11-07 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='address_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField(default=104.06, verbose_name='地图经度')),
                ('latitude', models.FloatField(default=30.69, verbose_name='地图纬度')),
                ('data', models.CharField(default=None, max_length=200)),
            ],
        ),
    ]
