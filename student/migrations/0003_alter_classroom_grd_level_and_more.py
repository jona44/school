# Generated by Django 5.0.1 on 2024-06-28 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '0007_gradelevel'),
        ('student', '0002_alter_attendance_academic_year_alter_classroom_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='grd_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.gradelevel'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='grade_level',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='district.gradelevel'),
        ),
    ]
