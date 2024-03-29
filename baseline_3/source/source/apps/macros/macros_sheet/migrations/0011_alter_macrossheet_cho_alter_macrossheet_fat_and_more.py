# Generated by Django 4.2.1 on 2023-07-01 14:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('macros_sheet', '0010_macrossheet_macros_planner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macrossheet',
            name='cho',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='macrossheet',
            name='fat',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='macrossheet',
            name='ptn',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
