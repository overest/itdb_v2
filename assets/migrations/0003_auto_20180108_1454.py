# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-08 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20171228_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinfo',
            name='check_time',
            field=models.DateTimeField(blank=True, null=True, unique=True, verbose_name='盘点时间'),
        ),
    ]
