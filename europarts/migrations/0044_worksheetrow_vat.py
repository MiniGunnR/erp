# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-06 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0043_worksheetrow_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheetrow',
            name='vat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]