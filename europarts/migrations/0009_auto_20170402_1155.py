# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-02 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0008_worksheet_quotation_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='recipient',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='recipient_address',
            field=models.CharField(default='', max_length=255),
        ),
    ]