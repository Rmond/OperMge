# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-22 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hd_ansible', '0008_auto_20170621_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sidinfo',
            name='result',
        ),
    ]
