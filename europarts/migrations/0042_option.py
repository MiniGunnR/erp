# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-16 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0041_delete_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
    ]
