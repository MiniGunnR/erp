# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-29 04:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0004_auto_20170328_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('part_no', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'Inventories',
            },
        ),
        migrations.AddField(
            model_name='worksheet',
            name='cost_price_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='sale_price_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='total_visible',
            field=models.BooleanField(default=True),
        ),
    ]
