# Generated by Django 5.0.6 on 2024-08-21 19:56

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customsettings', '0001_initial'),
        ('district', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_capacity', models.PositiveIntegerField(default=45)),
                ('date', models.DateField(auto_now_add=True)),
                ('class_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_class', to=settings.AUTH_USER_MODEL)),
                ('grd_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.gradelevel')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customsettings.classname')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.academiccalendar')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField(blank=True, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=255, null=True)),
                ('guardian_number', models.CharField(blank=True, max_length=15, null=True)),
                ('guardian_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.academiccalendar')),
                ('assigned_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.classroom')),
                ('grade_level', models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='district.gradelevel')),
                ('school_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customsettings.schoolprofile')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subjects', models.ManyToManyField(to='customsettings.schoolsubject')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, to='student.studentprofile'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='', max_length=10)),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.academiccalendar')),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
            ],
        ),
    ]
