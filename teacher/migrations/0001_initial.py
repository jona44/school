# Generated by Django 5.0.6 on 2024-08-21 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customsettings', '0001_initial'),
        ('district', '0001_initial'),
        ('student', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=20)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.academiccalendar')),
                ('assigned_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_class', to='student.classroom')),
                ('assigned_school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profiles', to='district.district_school_registration')),
                ('base_subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_subject_teacher_profiles', to='customsettings.schoolsubject')),
                ('classes_taught', models.ManyToManyField(related_name='teacher', to='student.classroom')),
                ('subjects_taught', models.ManyToManyField(related_name='teacher_subjects', to='customsettings.schoolsubject')),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
