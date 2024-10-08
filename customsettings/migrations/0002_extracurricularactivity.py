# Generated by Django 5.1 on 2024-09-14 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraCurricularActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('requirements', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('SP', 'Sports'), ('AR', 'Arts'), ('AC', 'Academic'), ('OT', 'Other')], max_length=2)),
                ('instructor', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
