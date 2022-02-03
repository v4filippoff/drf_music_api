from django.urls import path
from rest_framework.routers import SimpleRouter

from music_api.views import ListGenreView, ListGenreTracksView, TrackViewSet, ListUserTracksView, AlbumViewSet, \
    ListAlbumTracksView

router = SimpleRouter()
router.register('tracks', TrackViewSet)
router.register('albums', AlbumViewSet)

urlpatterns = [
    path('genres/', ListGenreView.as_view(), name='genre-list'),
    path('genres/<str:title>/tracks', ListGenreTracksView.as_view(), name='genre-track-list'),

    path('user-tracks/<int:user_id>', ListUserTracksView.as_view(), name='user-tracks-list'),
    path('album-tracks/<int:album_id>', ListAlbumTracksView.as_view(), name='album-tracks-list'),
]

urlpatterns += router.urls

