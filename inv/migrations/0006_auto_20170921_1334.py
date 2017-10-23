# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-21 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0005_auto_20170912_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='LCItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('count', models.CharField(max_length=20)),
                ('item', models.CharField(max_length=20)),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LetterOfCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('number', models.CharField(max_length=20)),
                ('spinning_mill', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lcitem',
            name='lc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.LetterOfCredit'),
        ),
    ]
