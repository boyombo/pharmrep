# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 03:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_sale_sales_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='sales_date',
        ),
    ]
