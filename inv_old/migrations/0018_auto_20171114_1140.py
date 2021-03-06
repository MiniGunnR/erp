# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-14 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0017_auto_20171114_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='yarnissue',
            name='finished_garments_quality',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yarnissue',
            name='grey_finished_dia',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yarnissue',
            name='knitting_factory_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yarnissue',
            name='machine_brand',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yarnissue',
            name='machine_dia',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yarnissue',
            name='machine_gauge',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
