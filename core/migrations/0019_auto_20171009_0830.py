# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-09 03:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170617_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 9, 3, 0, 14, 700000, tzinfo=utc)),
        ),
    ]
