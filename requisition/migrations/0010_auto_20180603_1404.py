# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-03 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0009_quotationrequest_quotationrequestitems'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuotationRequestItems',
            new_name='QuotationRequestItem',
        ),
    ]