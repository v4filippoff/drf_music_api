from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from music_api.models import Genre, Track
from music_api.permissions import IsAuthorOrReadOnly
from music_api.serializers import GenreSerializer, ViewTrackSerializer, CreateTrackSerializer


class ListGenreView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ListGenreTracksView(ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['title'])
        return genre.track_set.select_related('author', 'album').prefetch_related('genres')


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.select_related('author', 'album').prefetch_related('genres')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewTrackSerializer
        return CreateTrackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)