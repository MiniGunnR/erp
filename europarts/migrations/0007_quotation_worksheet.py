# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-31 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0006_auto_20170331_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='worksheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='europarts.Worksheet'),
            preserve_default=False,
        ),
    ]
