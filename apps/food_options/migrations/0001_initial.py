# Generated by Django 4.0.4 on 2024-08-25 17:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodOptions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('food', models.CharField(max_length=100)),
                ('quantity', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_of_measurement', models.CharField(choices=[('g', 'g'), ('U', 'U'), ('ml', 'ml')], default='g', max_length=50)),
                ('meal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='meal.meal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
