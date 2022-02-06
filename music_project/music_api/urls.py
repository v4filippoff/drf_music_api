from django.urls import path
from rest_framework.routers import SimpleRouter

from music_api.views import GenreListView, GenreTracksListView, TrackViewSet, UserTracksListView, AlbumViewSet, \
    AlbumTracksListView

router = SimpleRouter()
router.register('tracks', TrackViewSet)
router.register('albums', AlbumViewSet)

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),

    path('genre-tracks/<str:title>', GenreTracksListView.as_view(), name='genre-tracks-list'),
    path('user-tracks/<int:user_id>', UserTracksListView.as_view(), name='user-tracks-list'),
    path('album-tracks/<int:album_id>', AlbumTracksListView.as_view(), name='album-tracks-list'),
]

urlpatterns += router.urls

