# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-06 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0028_worksheetrow_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='barcode',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
