# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-14 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_ticket_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='denied',
            field=models.BooleanField(default=False),
        ),
    ]
