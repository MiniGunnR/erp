# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-14 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0019_auto_20171114_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='lcitem',
            name='unit',
            field=models.CharField(choices=[('kg', 'KG')], default='kg', max_length=2),
        ),
    ]
