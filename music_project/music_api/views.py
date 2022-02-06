from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from music_api.mixins import MusicEntityFilterBackendsMixin, SerializerSetMixin
from music_api.models import Genre, Track, Album
from music_api.permissions import IsAuthorOrReadOnly
from music_api.serializers import GenreSerializer, ViewTrackSerializer, CreateTrackSerializer, ViewAlbumSerializer, \
    CreateAlbumSerializer

User = get_user_model()


class GenreListView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreTracksListView(MusicEntityFilterBackendsMixin, ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['title'])
        return genre.track_set.all()


class TrackViewSet(SerializerSetMixin, MusicEntityFilterBackendsMixin, ModelViewSet):
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]
    serializer_set = {
        'read': ViewTrackSerializer,
        'write': CreateTrackSerializer
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTracksListView(MusicEntityFilterBackendsMixin, ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return Track.objects.filter(author=user)


class AlbumViewSet(SerializerSetMixin, MusicEntityFilterBackendsMixin, ModelViewSet):
    queryset = Album.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]
    serializer_set = {
        'read': ViewAlbumSerializer,
        'write': CreateAlbumSerializer
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AlbumTracksListView(MusicEntityFilterBackendsMixin, ListAPIView):
    serializer_class = ViewAlbumSerializer

    def get_queryset(self):
        album = get_object_or_404(Album, id=self.kwargs['album_id'])
        return Track.objects.filter(album=album)