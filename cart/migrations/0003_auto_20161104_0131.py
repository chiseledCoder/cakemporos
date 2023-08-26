# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20161009_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='commission_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='payout_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=50),
        ),
    ]
