# Generated by Django 4.0.6 on 2022-09-12 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('industries', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('directors', models.ManyToManyField(related_name='director_companies', to=settings.AUTH_USER_MODEL)),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='industries.industry')),
                ('managers', models.ManyToManyField(related_name='manager_companies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
