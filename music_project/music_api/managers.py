from django.db import models


class TrackManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'album').prefetch_related('genres')


class AlbumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('author').prefetch_related('genres')
