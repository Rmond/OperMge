# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-16 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0011_auto_20170615_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostinfo',
            name='idle',
            field=models.BooleanField(default=True),
        ),
    ]
