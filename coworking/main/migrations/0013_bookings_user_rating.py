# Generated by Django 5.0.4 on 2024-05-21 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_coworkingspaces_date_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='user_rating',
            field=models.BigIntegerField(default=0),
        ),
    ]