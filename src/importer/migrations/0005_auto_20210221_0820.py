# Generated by Django 3.1.6 on 2021-02-21 06:20

from django.db import migrations, models
import json.encoder


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0004_auto_20210221_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changes',
            name='additions',
            field=models.JSONField(blank=True, default=dict, encoder=json.encoder.JSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='changes',
            name='deletions',
            field=models.JSONField(blank=True, default=dict, encoder=json.encoder.JSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='changes',
            name='old_state',
            field=models.JSONField(blank=True, default=dict, encoder=json.encoder.JSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='changes',
            name='updates',
            field=models.JSONField(blank=True, default=dict, encoder=json.encoder.JSONEncoder, null=True),
        ),
    ]