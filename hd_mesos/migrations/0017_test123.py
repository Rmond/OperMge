# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hd_mesos', '0016_remove_user_task_softinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test123',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField(null=True)),
            ],
        ),
    ]
