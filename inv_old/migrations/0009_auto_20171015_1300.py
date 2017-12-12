# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-15 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0008_auto_20171004_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letterofcredit',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='yarnreceived',
            options={'ordering': ['lc_item']},
        ),
        migrations.AddField(
            model_name='yarnreceived',
            name='barcode',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]