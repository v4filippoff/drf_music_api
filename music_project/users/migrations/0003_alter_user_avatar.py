# Generated by Django 4.0.1 on 2022-01-31 18:10

import django.core.validators
from django.db import migrations, models
import users.services


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_follow_delete_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users.services.get_avatar_upload_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='User avatar'),
        ),
    ]