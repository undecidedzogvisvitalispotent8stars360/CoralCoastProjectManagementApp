# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0006_auto_20170627_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation_customers_documents',
            name='document_url_location',
        ),
    ]
