# Generated by Django 5.0.4 on 2024-05-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_bookings_id_alter_businesses_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesses',
            name='img',
            field=models.ImageField(default='upldfile/base_avatar.jpg', upload_to='upldfile/'),
        ),
        migrations.AddField(
            model_name='users',
            name='img',
            field=models.ImageField(default='upldfile/base_avatar.jpg', upload_to='upldfile/'),
        ),
    ]
