# Generated by Django 2.2.7 on 2021-02-02 05:55

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20210202_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_info',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
