# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-16 18:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_cart_total_cart_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_weight',
        ),
    ]
