# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-05 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('europarts', '0011_invoice_total_after_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ref_no', models.CharField(max_length=100)),
                ('recipient', models.CharField(default='', max_length=100)),
                ('recipient_address', models.CharField(default='', max_length=255)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='europarts.Invoice')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ChallanRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('part_no', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('challan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='europarts.Challan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
