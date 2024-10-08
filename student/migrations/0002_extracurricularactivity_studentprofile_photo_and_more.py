# Generated by Django 5.1 on 2024-09-13 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraCurricularActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('instructor', models.CharField(max_length=100)),
                ('requirements', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('SP', 'Sports'), ('AR', 'Arts'), ('AC', 'Academic'), ('OT', 'Other')], max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='photo',
            field=models.ImageField(default='media/students_photos/default.jpg', upload_to='media/students_photos'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='extra_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.extracurricularactivity'),
        ),
    ]
