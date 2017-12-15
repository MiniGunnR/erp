# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-15 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YarnIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('challan_no', models.CharField(max_length=20)),
                ('style', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('knitting_factory_name', models.CharField(max_length=100)),
                ('machine_brand', models.CharField(max_length=100)),
                ('machine_dia', models.CharField(max_length=100)),
                ('grey_finished_dia', models.CharField(max_length=100)),
                ('machine_gauge', models.CharField(max_length=100)),
                ('finished_garments_quality', models.CharField(max_length=100)),
                ('lc_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.LCItem')),
            ],
            options={
                'verbose_name_plural': 'Yarn Issue',
            },
        ),
    ]
