# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-18 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0023_auto_20170417_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksheetrow',
            name='part_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
