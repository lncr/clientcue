# Generated by Django 4.0.6 on 2022-09-12 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('industries', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name': 'Industry', 'verbose_name_plural': 'Industries'},
        ),
    ]
