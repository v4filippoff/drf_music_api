from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from music_api.models import Genre, Album, Track
from music_api.serializers import GenreSerializer, ViewTrackSerializer
from music_api.tests.utils import delete_tracks, add_testserver_prefix_to_track_files

User = get_user_model()


class GenreApiTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.genre = Genre.objects.create(title='classical')
        self.album = Album.objects.create(title='Album', author=self.user1)
        self.album.genres.add(self.genre)
        self.track1 = Track.objects.create(
            title='Track1',
            author=self.user1,
            file=SimpleUploadedFile('track1.wav', b'bbb')
        )
        self.track1.genres.add(self.genre)
        self.track2 = Track.objects.create(
            title='Track2',
            author=self.user2,
            file=SimpleUploadedFile('track2.mp3', b'uuu')
        )
        self.track2.genres.add(self.genre)

    def test_get_list(self):
        url = reverse('genre-list')
        response = self.client.get(url)
        genres = Genre.objects.all()
        serializer_data = GenreSerializer(genres, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_track_list(self):
        url = reverse('genre-track-list', args=(self.genre.title,))
        response = self.client.get(url)
        tracks = self.genre.track_set.all()
        serializer_data = ViewTrackSerializer(tracks, many=True).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_genre_404_not_found(self):
        url = reverse('genre-track-list', args=('fake-genre',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        delete_tracks(self.track1.file, self.track2.file)