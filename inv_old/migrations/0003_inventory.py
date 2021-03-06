# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inv', '0002_auto_20170827_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('uid', models.CharField(max_length=50, unique=True)),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
