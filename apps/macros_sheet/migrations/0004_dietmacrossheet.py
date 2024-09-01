# Generated by Django 4.0.4 on 2024-09-01 13:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0002_initial'),
        ('macros_sheet', '0003_mealmacrossheet_delete_macrossheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietMacrosSheet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('diet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='macros_sheet', to='diet.diet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
