# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-10 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_employeeleave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('attribute', models.CharField(max_length=50, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]