# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-08 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('europarts', '0027_quotationrow_display_id'), ('europarts', '0028_auto_20180408_1217'), ('europarts', '0029_auto_20180408_1226'), ('europarts', '0030_auto_20180408_1226'), ('europarts', '0031_auto_20180408_1228'), ('europarts', '0032_auto_20180408_1257')]

    dependencies = [
        ('europarts', '0026_auto_20170418_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='display_id',
            field=models.IntegerField(default=5),
        ),
    ]
