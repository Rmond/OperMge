# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0012_hostinfo_idle'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_task',
            name='softinfo',
            field=models.CharField(default='', max_length=32),
        ),
    ]
