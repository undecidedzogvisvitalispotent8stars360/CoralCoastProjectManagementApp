# Generated by Django 2.1.5 on 2019-02-01 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0010_auto_20190131_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='quote_approval_status_id',
        ),
    ]
