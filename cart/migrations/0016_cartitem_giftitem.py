# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-13 04:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20171009_0842'),
        ('cart', '0015_auto_20171013_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='giftitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.GiftItem'),
        ),
    ]
