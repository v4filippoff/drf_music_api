from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status

from music_api.models import Genre, Album, Track
from music_api.serializers import GenreSerializer, ViewTrackSerializer, ViewAlbumSerializer
from music_api.tests.utils import remove_test_media_dir, add_testserver_prefix_to_track_files

User = get_user_model()


@override_settings(MEDIA_ROOT=settings.TEST_MEDIA_ROOT)
class BaseMusicApiTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='user1@gmail.com')
        self.user2 = User.objects.create(username='user2', email='user2@gmail.com')
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

    def tearDown(self):
        remove_test_media_dir()


class GenreApiTestCase(BaseMusicApiTestCase):

    def test_get_list(self):
        url = reverse('genre-list')
        response = self.client.get(url)
        genres = Genre.objects.all()
        serializer_data = GenreSerializer(genres, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)

    def test_get_track_list(self):
        url = reverse('genre-tracks-list', args=(self.genre.title,))
        response = self.client.get(url)
        tracks = self.genre.track_set.all()
        serializer_data = ViewTrackSerializer(tracks, many=True).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)

    def test_genre_404_not_found(self):
        url = reverse('genre-tracks-list', args=('fake-genre',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TrackApiTestCase(BaseMusicApiTestCase):

    def test_get_list(self):
        url = reverse('track-list')
        response = self.client.get(url)
        tracks = Track.objects.all()
        serializer_data = ViewTrackSerializer(tracks, many=True).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)

    def test_create(self):
        url = reverse('track-list')
        data = {
            'title': 'New track',
            'genres': [self.genre.id],
            'file': SimpleUploadedFile('new_track.mp3', b'eee')
        }
        self.client.force_login(self.user1)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 3)
        self.assertEqual(Track.objects.last().author, self.user1)

    def test_detail(self):
        url = reverse('track-detail', args=(self.track1.id,))
        response = self.client.get(url)
        track = Track.objects.filter(id=self.track1.id).get()
        serializer_data = ViewTrackSerializer(track).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_partial_update(self):
        url = reverse('track-detail', args=(self.track1.id,))
        data = {
            'title': 'Super new track',
        }
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=data, content_type='application/json')
        self.track1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.track1.title)

    def test_delete(self):
        url = reverse('track-detail', args=(self.track1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Track.objects.count(), 1)
        self.assertFalse(Track.objects.filter(id=self.track1.id).exists())

    def test_partial_update_not_author(self):
        url = reverse('track-detail', args=(self.track1.id,))
        data = {
            'title': 'Super new track',
        }
        self.client.force_login(self.user2)
        response = self.client.patch(url, data=data, content_type='application/json')
        self.track1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.track1.title, 'Track1')

    def test_delete_not_author(self):
        url = reverse('track-detail', args=(self.track1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Track.objects.count(), 2)
        self.assertTrue(Track.objects.filter(id=self.track1.id).exists())

    def test_get_user_tracks(self):
        url = reverse('user-tracks-list', args=(self.user1.id,))
        response = self.client.get(url)
        tracks = Track.objects.filter(author=self.user1)
        serializer_data = ViewTrackSerializer(tracks, many=True).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)

    def test_get_album_tracks(self):
        url = reverse('album-tracks-list', args=(self.album.id,))
        response = self.client.get(url)
        tracks = Track.objects.filter(album=self.album)
        serializer_data = ViewTrackSerializer(tracks, many=True).data
        add_testserver_prefix_to_track_files(serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)


class AlbumApiTestCase(BaseMusicApiTestCase):

    def test_get_list(self):
        url = reverse('album-list')
        response = self.client.get(url)
        albums = Album.objects.all()
        serializer_data = ViewAlbumSerializer(albums, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer_data)

    def test_create(self):
        url = reverse('album-list')
        data = {
            'title': 'New album',
            'genres': [self.genre.id],
        }
        self.client.force_login(self.user1)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(Album.objects.last().author, self.user1)

    def test_detail(self):
        url = reverse('album-detail', args=(self.album.id,))
        response = self.client.get(url)
        album = Album.objects.filter(id=self.album.id).get()
        serializer_data = ViewAlbumSerializer(album).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_update(self):
        url = reverse('album-detail', args=(self.album.id,))
        data = {
            'title': 'Super new album',
            'genres': [self.genre.id]
        }
        self.client.force_login(self.user1)
        response = self.client.put(url, data=data, content_type='application/json')
        self.album.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.album.title)

    def test_delete(self):
        url = reverse('album-detail', args=(self.album.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    def test_update_not_author(self):
        url = reverse('album-detail', args=(self.album.id,))
        data = {
            'title': 'Super new album',
            'genres': [self.genre.id]
        }
        self.client.force_login(self.user2)
        response = self.client.put(url, data=data, content_type='application/json')
        self.album.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.album.title, 'Album')

    def test_delete_not_author(self):
        url = reverse('album-detail', args=(self.album.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Album.objects.count(), 1)
        self.assertTrue(Album.objects.filter(id=self.album.id).exists())