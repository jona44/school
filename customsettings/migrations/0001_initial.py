# Generated by Django 5.0.6 on 2024-08-21 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('district', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_logo', models.ImageField(blank=True, null=True, upload_to='school_logos/')),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('is_setup_complete', models.BooleanField(default=False)),
                ('school_name', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.district_school_registration')),
            ],
        ),
        migrations.CreateModel(
            name='ClassName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('academic_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.academiccalendar')),
                ('grd_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.gradelevel')),
                ('schoolprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customsettings.schoolprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolprofile_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customsettings.schoolprofile')),
                ('subjects', models.ManyToManyField(to='district.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='schoolprofile',
            name='school_subjects',
            field=models.ManyToManyField(to='customsettings.schoolsubject'),
        ),
    ]
