# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-21 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0009_auto_20170319_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='recipient',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quotation',
            name='recipient_address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationcode',
            name='code',
            field=models.CharField(default='114679', max_length=6),
        ),
    ]