# Generated by Django 4.0.6 on 2022-10-20 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('industries', '0002_alter_industry_options'),
        ('companies', '0002_alter_company_options_alter_company_directors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='industry_company', to='industries.industry'),
        ),
    ]
