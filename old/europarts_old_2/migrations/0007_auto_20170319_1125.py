# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-19 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0006_auto_20170306_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationcode',
            name='code',
            field=models.CharField(default='204847', max_length=6),
        ),
    ]
