# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-08 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0027_quotationrow_display_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationrow',
            name='display_id',
            field=models.IntegerField(default=5),
        ),
    ]
