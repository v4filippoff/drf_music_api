from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from music_api.generics import MusicEntityViewSet
from music_api.models import Genre, Track, Album
from music_api.serializers import GenreSerializer, ViewTrackSerializer, CreateTrackSerializer, ViewAlbumSerializer, \
    CreateAlbumSerializer

User = get_user_model()


class ListGenreView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ListGenreTracksView(ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['title'])
        return genre.track_set.select_related('author', 'album').prefetch_related('genres')


class TrackViewSet(MusicEntityViewSet):
    queryset = Track.objects.all()
    serializer_set = {
        'read': ViewTrackSerializer,
        'write': CreateTrackSerializer
    }


class ListUserTracksView(ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return Track.objects.filter(author=user)


class AlbumViewSet(MusicEntityViewSet):
    queryset = Album.objects.all()
    serializer_set = {
        'read': ViewAlbumSerializer,
        'write': CreateAlbumSerializer
    }


class ListAlbumTracksView(ListAPIView):
    serializer_class = ViewAlbumSerializer

    def get_queryset(self):
        album = get_object_or_404(Album, id=self.kwargs['album_id'])
        return Track.objects.filter(album=album)