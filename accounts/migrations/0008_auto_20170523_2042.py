# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-23 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_useraddresses_user_locality'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraddresses',
            options={'verbose_name_plural': "User's Shipping Addresses"},
        ),
    ]
