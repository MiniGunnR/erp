# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-17 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0017_auto_20170417_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='ship_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]