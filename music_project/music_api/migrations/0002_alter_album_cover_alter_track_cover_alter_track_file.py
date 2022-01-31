# Generated by Django 4.0.1 on 2022-01-31 18:10

import django.core.validators
from django.db import migrations, models
import music_api.services


class Migration(migrations.Migration):

    dependencies = [
        ('music_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=music_api.services.get_album_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='Album cover'),
        ),
        migrations.AlterField(
            model_name='track',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=music_api.services.get_track_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='Track cover'),
        ),
        migrations.AlterField(
            model_name='track',
            name='file',
            field=models.FileField(upload_to=music_api.services.get_track_upload_path, validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav'])], verbose_name='Track file'),
        ),
    ]
