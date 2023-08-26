# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('bakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coupon_title', models.CharField(max_length=200)),
                ('coupon_code', models.CharField(max_length=20)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('min_cart_value', models.IntegerField(default=b'0')),
                ('discount_type', models.CharField(default=b'', max_length=20, choices=[(b'Fixed Amount', b'Fixed Amount'), (b'Percentage', b'Percentage')])),
                ('coupon_cost', models.IntegerField(default=b'0')),
                ('usage_per_person', models.IntegerField(default=b'1')),
                ('max_usage', models.IntegerField(null=True, blank=True)),
                ('bakers', models.ForeignKey(blank=True, to='bakers.Baker', null=True)),
                ('categories', models.ForeignKey(blank=True, to='catalog.Category', null=True)),
                ('products', models.ForeignKey(blank=True, to='catalog.Product', null=True)),
            ],
        ),
    ]
