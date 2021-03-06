# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 02:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_sale_amount'),
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('address', models.TextField(blank=True)),
                ('rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Rep')),
            ],
        ),
    ]
