# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 11:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0015_auto_20170619_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_task',
            name='softinfo',
        ),
    ]
