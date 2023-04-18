# Generated by Django 3.1.8 on 2022-11-27 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailtemplates', '0003_auto_20220911_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtemplate',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='URL amigable'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Asunto'),
        ),
    ]
