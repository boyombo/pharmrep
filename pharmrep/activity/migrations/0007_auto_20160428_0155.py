# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 01:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_itinerary_summary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itinerary',
            options={'verbose_name_plural': 'Itinerary'},
        ),
        migrations.AlterModelOptions(
            name='summary',
            options={'verbose_name_plural': 'Summaries'},
        ),
    ]
