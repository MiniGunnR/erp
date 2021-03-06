# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('europarts_old_2', '0004_auto_20170205_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='list',
            options={'permissions': (('can_add_product_list', 'Can add product list'),)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': (('can_view_cost_price', 'Can view cost price'), ('can_add_cost_price', 'Can add cost price'), ('can_edit_cost_price', 'Can edit cost price'), ('can_view_selling_price', 'Can view selling price'), ('can_add_selling_price', 'Can add selling price'), ('can_edit_selling_price', 'Can edit selling price'))},
        ),
        migrations.AddField(
            model_name='list',
            name='cost_price_quoted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='list',
            name='selling_price_quoted',
            field=models.BooleanField(default=False),
        ),
    ]
