# Generated by Django 4.0.4 on 2024-08-31 20:17

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('goal', models.CharField(blank=True, max_length=100)),
                ('observations', models.CharField(blank=True, max_length=300)),
                ('initial_date', models.DateField()),
                ('final_date', models.DateField()),
                ('weeks', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('type_of_diet', models.CharField(choices=[('Maintenance', 'Maintenance'), ('Bulking', 'Bulking'), ('Cutting', 'Cutting')], default='Maintenance', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
