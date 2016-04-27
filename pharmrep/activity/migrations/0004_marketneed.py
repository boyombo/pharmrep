# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 02:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_sale_amount'),
        ('activity', '0003_contact_added_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketNeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('recorded_date', models.DateField(default=datetime.date.today)),
                ('rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Rep')),
            ],
        ),
    ]
