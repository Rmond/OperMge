# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0019_auto_20170630_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='vginfo',
            field=models.TextField(null=True),
        ),
    ]
