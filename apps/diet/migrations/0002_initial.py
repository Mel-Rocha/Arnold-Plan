# Generated by Django 4.0.4 on 2024-08-31 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('diet', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diet',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.athlete'),
        ),
        migrations.AddField(
            model_name='diet',
            name='nutritionist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.nutritionist'),
        ),
    ]