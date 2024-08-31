# Generated by Django 4.0.4 on 2024-08-31 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0001_initial'),
        ('meal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='diet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='diet.diet'),
        ),
    ]