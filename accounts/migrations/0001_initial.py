# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_corporate', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,12}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")])),
                ('user_otp', models.IntegerField(null=True, blank=True)),
                ('user_otp_session', models.CharField(max_length=100, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('coupon', models.ManyToManyField(default=b'', to='sales.Coupon')),
                ('user', models.OneToOneField(related_name='userprofile', to=settings.AUTH_USER_MODEL)),
                ('user_locality', models.ForeignKey(blank=True, to='core.Locality', null=True)),
            ],
            options={
                'verbose_name_plural': 'User Accounts',
            },
        ),
        migrations.CreateModel(
            name='UserAddresses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_addresses', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'User Shipping Addresses',
            },
        ),
    ]
