# Generated by Django 3.1.8 on 2022-09-11 17:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendas', '0003_auto_20210423_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='year',
            field=models.IntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(9999)], verbose_name='Año'),
        ),
    ]
