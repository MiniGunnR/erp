# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-09 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0034_auto_20180808_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='europarts.Client'),
        ),
    ]
