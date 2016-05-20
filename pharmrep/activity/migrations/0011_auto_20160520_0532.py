# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20160518_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itinerary',
            name='places',
        ),
        migrations.AddField(
            model_name='itinerary',
            name='activity',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='time_slot',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '8am-9am'), (1, '9am-10am'), (2, '10am-11am'), (3, '11am-12noon'), (4, '12noon-1pm'), (5, '1pm-2pm'), (6, '2pm-3pm'), (7, '3pm-4pm'), (8, '4pm-5pm'), (9, 'After 5pm')], null=True),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='call',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_products', to='activity.Call'),
        ),
    ]
