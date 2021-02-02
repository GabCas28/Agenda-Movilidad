# Generated by Django 2.2.7 on 2021-02-02 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendas', '0002_auto_20210117_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='description',
            field=models.TextField(verbose_name=''),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='slug',
            field=models.SlugField(verbose_name=''),
        ),
    ]
