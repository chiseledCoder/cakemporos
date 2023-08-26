# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Baker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_address', models.TextField(default=b'', max_length=250)),
                ('baker_type', models.CharField(default=b'Local', max_length=10, choices=[(b'Home', b'Home'), (b'Local', b'Local')])),
                ('shop_name', models.CharField(default=b'', max_length=50)),
                ('shop_pno', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,12}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")])),
                ('shop_address', models.TextField(default=b'', max_length=250)),
                ('veg_or_nonveg', models.CharField(default=b'Both', max_length=100, choices=[(b'Both', b'Both'), (b'Only Vegeterian', b'Only Vegeterian'), (b'Only Non-Vegeterian', b'Only Non-Vegeterian')])),
                ('min_order_time', models.CharField(default=b'', max_length=50, choices=[(b'0-3 Hrs', b'0-3 Hrs'), (b'3-6 Hrs', b'3-6 Hrs'), (b'6-9Hrs', b'6-9Hrs'), (b'Above 12 Hrs', b'Above 12 Hrs')])),
                ('image', models.ImageField(default=b'baker/default.jpg', upload_to=b'baker/images/')),
                ('shop_license_number', models.CharField(default=b'', max_length=500, blank=True)),
                ('mou_signed_on', models.DateField(verbose_name=b'Date')),
                ('featured', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'Disabled', max_length=100, choices=[(b'Enabled', b'Enabled'), (b'Disabled', b'Disabled')])),
                ('customized_cake_option', models.BooleanField(default=False)),
                ('photo_cake_option', models.BooleanField(default=False)),
                ('min_weight_for_customization', models.CharField(default=b'0.5 and above', max_length=200, choices=[(b'0.5 Kg and above', b'0.5 Kg and above'), (b'1 Kg and above', b'1 Kg and above'), (b'1.5 Kg and above', b'1.5 Kg and above')])),
                ('min_weight_for_photocake', models.CharField(default=b'0.5 and above', max_length=200, choices=[(b'0.5 Kg and above', b'0.5 Kg and above'), (b'1 Kg and above', b'1 Kg and above'), (b'1.5 Kg and above', b'1.5 Kg and above')])),
                ('slug', models.SlugField(unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(related_name='baker', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('shop_locality', models.ForeignKey(default=b'', to='core.Locality')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
