# Generated by Django 4.2.1 on 2023-07-01 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20210421_0245'),
        ('mailsender', '0002_auto_20210421_0245'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultadoDifusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado_del_envio', models.BooleanField()),
                ('contacto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.contact')),
            ],
        ),
    ]
