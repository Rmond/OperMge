# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0010_auto_20170615_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_task',
            name='date_done',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user_task',
            name='result',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user_task',
            name='status',
            field=models.CharField(default='Running', max_length=50),
        ),
    ]
