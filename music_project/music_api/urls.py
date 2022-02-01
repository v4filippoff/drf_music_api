from django.urls import path

from music_api.views import ListGenreView, ListGenreTracksView

urlpatterns = [
    path('genres/', ListGenreView.as_view(), name='genre-list'),
    path('genres/<str:title>/tracks', ListGenreTracksView.as_view(), name='genre-track-list'),
]

