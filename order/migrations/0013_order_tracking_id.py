# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20161115_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]