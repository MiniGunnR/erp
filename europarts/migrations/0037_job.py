# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-14 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0036_challan_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('job_no', models.CharField(max_length=100)),
                ('appointment_date', models.DateField()),
                ('client_name', models.CharField(max_length=255)),
                ('client_address', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
