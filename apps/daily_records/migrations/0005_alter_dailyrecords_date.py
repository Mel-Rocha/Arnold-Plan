# Generated by Django 4.0.4 on 2024-09-01 15:16

import apps.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_records', '0004_alter_dailyrecords_meal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyrecords',
            name='date',
            field=models.DateField(validators=[apps.core.validators.validate_not_in_future]),
        ),
    ]
