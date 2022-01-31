from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from music_api.services import get_track_cover_upload_path, get_track_upload_path, get_album_cover_upload_path

User = get_user_model()


class Genre(models.Model):
    """
    Жанр музыки
    """
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'Genre: {self.title}'


class Album(models.Model):
    """
    Альбом с треками
    """
    authors = models.ManyToManyField(User, related_name='albums')
    title = models.CharField('Title', max_length=50)
    genres = models.ManyToManyField(Genre, related_name='albums')
    date_added = models.DateField('Date added', auto_now_add=True)
    cover = models.ImageField(
        'Album cover',
        upload_to=get_album_cover_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    plays_count = models.PositiveIntegerField('Plays count', default=0)

    def __str__(self):
        return 'Album: {0} ({1})'.format(
            self.title,
            ', '.join(author.name for author in self.authors.all())
        )


class Track(models.Model):
    """
    Музыкальный трек
    """
    authors = models.ManyToManyField(User, related_name='tracks')
    title = models.CharField('Title', max_length=50)
    genres = models.ManyToManyField(Genre, related_name='tracks')
    date_added = models.DateField('Date added', auto_now_add=True)
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
    plays_count = models.PositiveIntegerField('Plays count', default=0)
    downloads_count = models.PositiveIntegerField('Downloads count', default=0)

    def __str__(self):
        return 'Track: {0} ({1})'.format(
            self.title,
            ', '.join(author.name for author in self.authors.all())
        )
