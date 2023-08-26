# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxVariations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('box_variation_type', models.CharField(default=b'1 Box', max_length=100, choices=[(b'1 Box', b'1 Box'), (b'2 Box', b'2 Box'), (b'3 Box', b'3 Box'), (b'4 Box', b'4 Box'), (b'5 Box', b'5 Box'), (b'6 Box', b'6 Box')])),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CakeCustomization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('starting_weight', models.CharField(default=b'0.5 Kg', max_length=100, choices=[(b'0.5 Kg', b' 0.5 Kg'), (b'1 Kg', b'1 Kg'), (b'1.5 Kg', b' 1.5 Kg'), (b'2 Kg', b'2 Kg')])),
                ('starting_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('baker', models.ForeignKey(default=b'', to='bakers.Baker')),
            ],
        ),
        migrations.CreateModel(
            name='CakeOfTheDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Cake of the Day',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EggVariations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('egg_variation_type', models.CharField(default=b'Eggless', max_length=100, choices=[(b'Egg', b'Egg'), (b'Eggless', b'Eggless')])),
                ('extra_price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoCakeCustomization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.CharField(default=b'0.5 Kg', max_length=100, choices=[(b'0.5 Kg', b' 0.5 Kg'), (b'1 Kg', b'1 Kg'), (b'1.5 Kg', b' 1.5 Kg'), (b'2 Kg', b'2 Kg')])),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('baker', models.ForeignKey(default=b'', to='bakers.Baker')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('image', models.ImageField(default=b'products/default.jpg', upload_to=b'products/images/')),
                ('veg_or_nonveg', models.CharField(default=b'Both', max_length=100, choices=[(b'Both', b'Both'), (b'Only Vegeterian', b'Only Vegeterian'), (b'Only Non-Vegeterian', b'Only Non-Vegeterian')])),
                ('status', models.CharField(default=b'Disabled', max_length=100, choices=[(b'Enabled', b'Enabled'), (b'Disabled', b'Disabled')])),
                ('slug', models.SlugField(max_length=200, unique=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('baker', models.ForeignKey(blank=True, to='bakers.Baker', null=True)),
                ('category', models.ForeignKey(blank=True, to='catalog.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeightVariations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight_variation_type', models.CharField(default=b'0.5 Kg', max_length=100, choices=[(b'0.5 Kg', b' 0.5 Kg'), (b'1 Kg', b'1 Kg'), (b'1.5 Kg', b' 1.5 Kg'), (b'2 Kg', b'2 Kg')])),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default=b'', blank=True, to='catalog.Product', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, to='catalog.ProductType', null=True),
        ),
        migrations.AddField(
            model_name='eggvariations',
            name='product',
            field=models.ForeignKey(default=b'', blank=True, to='catalog.Product', null=True),
        ),
        migrations.AddField(
            model_name='cakeoftheday',
            name='cake',
            field=models.ForeignKey(default=b'', blank=True, to='catalog.Product', null=True),
        ),
        migrations.AddField(
            model_name='boxvariations',
            name='product',
            field=models.ForeignKey(default=b'', blank=True, to='catalog.Product', null=True),
        ),
    ]
