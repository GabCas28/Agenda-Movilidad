# Generated by Django 3.1.6 on 2021-03-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailtemplates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtemplate',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]