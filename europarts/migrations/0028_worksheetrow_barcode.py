# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-06 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0027_quotationrow_display_id_squashed_0032_auto_20180408_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheetrow',
            name='barcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
