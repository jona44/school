# Generated by Django 5.0.1 on 2024-06-19 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0003_schoolsubject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolprofile',
            old_name='shool_subjects',
            new_name='school_subjects',
        ),
    ]
