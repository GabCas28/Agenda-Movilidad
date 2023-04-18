# Generated by Django 3.1.8 on 2023-01-29 22:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendas', '0004_auto_20220911_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='year',
            field=models.IntegerField(default=2023, validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(9999)], verbose_name='Año'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL'),
        ),
    ]
