# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-06 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0015_auto_20180425_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_of_quote_stages',
            name='quote_closed',
            field=models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=5),
        ),
    ]