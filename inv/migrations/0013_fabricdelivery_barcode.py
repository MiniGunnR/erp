# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-15 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0012_yarndelivery_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabricdelivery',
            name='barcode',
            field=models.CharField(default='000000000000', max_length=50),
        ),
    ]
