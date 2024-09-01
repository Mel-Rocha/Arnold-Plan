# Generated by Django 4.0.4 on 2024-08-31 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0001_initial'),
        ('daily_records', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyrecords',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_records', to='meal.meal'),
        ),
    ]