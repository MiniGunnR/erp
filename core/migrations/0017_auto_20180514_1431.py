# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-14 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_mail_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='body',
            field=models.TextField(default=b'Dear Sir,\n\nPlease find the attached file.\n\nSincerely yours,\nMd Sorower Hossain'),
        ),
    ]
