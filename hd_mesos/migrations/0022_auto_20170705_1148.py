# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-05 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0021_auto_20170705_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostinfo',
            name='memory_free',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hostinfo',
            name='memory_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hostinfo',
            name='memory_used',
            field=models.IntegerField(null=True),
        ),
    ]
