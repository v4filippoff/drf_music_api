from django.urls import path
from rest_framework.routers import SimpleRouter

from music_api.views import ListGenreView, ListGenreTracksView, TrackViewSet

router = SimpleRouter()
router.register('tracks', TrackViewSet)

urlpatterns = [
    path('genres/', ListGenreView.as_view(), name='genre-list'),
    path('genres/<str:title>/tracks', ListGenreTracksView.as_view(), name='genre-track-list'),
]

urlpatterns += router.urls

