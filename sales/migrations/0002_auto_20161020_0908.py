# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
