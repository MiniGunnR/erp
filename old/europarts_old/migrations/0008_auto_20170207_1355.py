# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 07:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0007_auto_20170206_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('part_no', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='list',
            options={'ordering': ['-created'], 'permissions': (('can_add_product_list', 'Can add product list'),)},
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='part_no',
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(default='pcs', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='car_part',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='europarts.CarPart'),
            preserve_default=False,
        ),
    ]
