# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-03 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180514_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='body',
            field=models.TextField(default=''),
        ),
    ]
