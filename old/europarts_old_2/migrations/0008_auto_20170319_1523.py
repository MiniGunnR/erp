# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-19 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0007_auto_20170319_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationcode',
            name='code',
            field=models.CharField(default='182293', max_length=6),
        ),
    ]