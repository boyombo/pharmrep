# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20160430_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='price_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.PriceTemplate'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.IntegerField(verbose_name='Default price of product'),
        ),
    ]
