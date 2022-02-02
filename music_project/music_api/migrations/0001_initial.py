# Generated by Django 4.0.1 on 2022-02-01 18:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import music_api.services


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Date added')),
                ('plays_count', models.PositiveIntegerField(default=0, verbose_name='Plays count')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=music_api.services.get_album_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='Album cover')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Date added')),
                ('plays_count', models.PositiveIntegerField(default=0, verbose_name='Plays count')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=music_api.services.get_track_cover_upload_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='Track cover')),
                ('file', models.FileField(upload_to=music_api.services.get_track_upload_path, validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav'])], verbose_name='Track file')),
                ('downloads_count', models.PositiveIntegerField(default=0, verbose_name='Downloads count')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='music_api.album')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('genres', models.ManyToManyField(to='music_api.Genre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(to='music_api.Genre'),
        ),
    ]
