from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from music_api.managers import AlbumManager, TrackManager
from music_api.services import get_track_cover_upload_path, get_track_upload_path, get_album_cover_upload_path

User = get_user_model()


class Genre(models.Model):
    """
    Жанр музыки
    """
    title = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Genre: {self.title}'


class MusicEntity(models.Model):
    """
    Абстрактная музыкальная сущность
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=50)
    genres = models.ManyToManyField(Genre)
    date_added = models.DateField('Date added', auto_now_add=True)
    plays_count = models.PositiveIntegerField('Plays count', default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return '{0}: {1} ({2})'.format(
            self._meta.model_name.title(),
            self.title,
            self.author.username
        )


class Album(MusicEntity):
    """
    Альбом с треками
    """
    cover = models.ImageField(
        'Album cover',
        upload_to=get_album_cover_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    objects = AlbumManager()


class Track(MusicEntity):
    """
    Музыкальный трек
    """
    cover = models.ImageField(
        'Track cover',
        upload_to=get_track_cover_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    file = models.FileField(
        'Track file',
        upload_to=get_track_upload_path,
        validators=[FileExtensionValidator(['mp3', 'wav'])]
    )
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    downloads_count = models.PositiveIntegerField('Downloads count', default=0)

    objects = TrackManager()
