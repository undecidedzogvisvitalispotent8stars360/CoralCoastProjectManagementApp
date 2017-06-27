# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NearBeach', '0004_auto_20170627_0715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation_customers_documents',
            name='document_folder_id',
        ),
        migrations.AddField(
            model_name='organisation_customers_documents',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project_tasks_documents',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
