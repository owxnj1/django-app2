# Generated by Django 5.1.2 on 2025-01-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/profile_pics/default.jpg', upload_to='profile_pics'),
        ),
    ]