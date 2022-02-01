from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from music_api.models import Track, Album, Genre

User = get_user_model()


class GenreSerializer(ModelSerializer):
    """
    Сериализатор жанра музыки
    """
    class Meta:
        model = Genre
        fields = '__all__'


class MusicAuthorSerializer(ModelSerializer):
    """
    Сериализатор авторов музыкального контента
    """
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class CreateAlbumSerializer(ModelSerializer):
    """
    Сериализатор для создания альбома
    """
    class Meta:
        model = Album
        fields = (
            'id',
            'title',
            'authors',
            'genres',
            'date_added',
            'cover',
            'plays_count',
        )
        read_only_fields = ('date_added', 'plays_count')


class ViewAlbumSerializer(CreateAlbumSerializer):
    """
    Сериализатор для просмотра альбома
    """
    authors = MusicAuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class SimpleViewAlbumSerializer(ModelSerializer):
    """
    Упрощенный сериализатор для просмотра альбомов
    """
    class Meta:
        model = Album
        fields = (
            'id',
            'title'
        )


class CreateTrackSerializer(ModelSerializer):
    """
    Сериализатор для создания трека
    """
    class Meta:
        model = Track
        fields = (
            'id',
            'title',
            'authors',
            'genres',
            'date_added',
            'cover',
            'plays_count',
            'file',
            'album',
            'downloads_count',
        )
        read_only_fields = ('date_added', 'plays_count', 'downloads_count')


class ViewTrackSerializer(CreateTrackSerializer):
    """
    Сериализатор для просмотра трека
    """
    authors = MusicAuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    album = SimpleViewAlbumSerializer(read_only=True)
