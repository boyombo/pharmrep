# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 03:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20160501_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rep',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
