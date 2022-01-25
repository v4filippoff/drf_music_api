from django.contrib import admin

from music_api.models import Genre, Album, Track


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date_added',
        'plays_count',
    )


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date_added',
        'plays_count',
        'downloads_count',
    )
