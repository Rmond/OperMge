# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0002_auto_20170601_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_task',
            name='host_group',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]