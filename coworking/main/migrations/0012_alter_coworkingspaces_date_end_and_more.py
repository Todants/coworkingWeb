# Generated by Django 5.0.4 on 2024-05-18 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_coworkingspaces_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coworkingspaces',
            name='date_end',
            field=models.TimeField(default='22:00:00'),
        ),
        migrations.AlterField(
            model_name='coworkingspaces',
            name='date_start',
            field=models.TimeField(default='10:00:00'),
        ),
    ]
