# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0005_auto_20170609_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostinfo',
            name='tags',
            field=models.CharField(default='', max_length=64),
        ),
    ]
