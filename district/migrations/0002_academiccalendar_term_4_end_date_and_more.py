# Generated by Django 5.0.6 on 2024-09-08 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='academiccalendar',
            name='term_4_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='academiccalendar',
            name='term_4_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
