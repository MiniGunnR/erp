# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-24 15:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Mail',
        ),
    ]
