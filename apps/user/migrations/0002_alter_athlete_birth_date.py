# Generated by Django 4.0.4 on 2024-09-01 15:12

import apps.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='birth_date',
            field=models.DateField(validators=[apps.core.validators.validate_not_in_future]),
        ),
    ]