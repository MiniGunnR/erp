# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-17 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0019_auto_20170417_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='part',
            name='type',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='type',
            field=models.CharField(blank=True, choices=[('Vehicle', 'Vehicle'), ('Marine', 'Marine')], max_length=50, null=True),
        ),
    ]