# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-16 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_cart_delivery_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_weight',
            field=models.CharField(choices=[(b'0.5 Kg', b' 0.5 Kg'), (b'1 Kg', b'1 Kg'), (b'1.5 Kg', b' 1.5 Kg'), (b'2 Kg', b'2 Kg')], default=b'Both', max_length=100),
        ),
    ]
