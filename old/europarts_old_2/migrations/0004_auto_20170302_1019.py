# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-02 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0003_auto_20170228_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationproduct',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationcode',
            name='code',
            field=models.CharField(default='261178', max_length=6),
        ),
    ]