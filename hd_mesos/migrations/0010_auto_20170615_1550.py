# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0009_auto_20170614_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_task',
            name='star_time',
            field=models.DateTimeField(),
        ),
    ]
