# Generated by Django 4.0.4 on 2024-09-01 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('macros_sheet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='macrossheet',
            name='week',
        ),
    ]
