# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170205_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
