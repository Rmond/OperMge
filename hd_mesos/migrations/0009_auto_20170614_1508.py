# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0008_auto_20170614_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_task',
            name='taskid',
            field=models.CharField(default='', max_length=48),
        ),
    ]