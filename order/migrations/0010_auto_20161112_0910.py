# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-12 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_approve'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderhistory',
            old_name='approval',
            new_name='approve',
        ),
        migrations.AddField(
            model_name='order',
            name='notify_baker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='notify_customer',
            field=models.BooleanField(default=False),
        ),
    ]