# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-11 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0021_auto_20171116_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fabricdelivery',
            name='yd',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='lcitem',
            name='lc',
        ),
        migrations.RemoveField(
            model_name='yarnissue',
            name='yr',
        ),
        migrations.RemoveField(
            model_name='yarnreceived',
            name='lc_item',
        ),
        migrations.DeleteModel(
            name='FabricDelivery',
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
        migrations.DeleteModel(
            name='LCItem',
        ),
        migrations.DeleteModel(
            name='LetterOfCredit',
        ),
        migrations.DeleteModel(
            name='YarnIssue',
        ),
        migrations.DeleteModel(
            name='YarnReceived',
        ),
    ]