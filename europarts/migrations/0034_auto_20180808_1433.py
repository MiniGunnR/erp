# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-08 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0033_auto_20180808_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
