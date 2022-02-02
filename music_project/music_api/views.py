from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from music_api.models import Genre
from music_api.serializers import GenreSerializer, ViewTrackSerializer


class ListGenreView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ListGenreTracksView(ListAPIView):
    serializer_class = ViewTrackSerializer

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['title'])
        return genre.track_set.select_related('author', 'album').prefetch_related('genres')
