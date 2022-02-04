from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from music_api.models import Genre, Album, Track
from music_api.serializers import GenreSerializer, MusicAuthorSerializer, CreateAlbumSerializer, ViewAlbumSerializer, \
    SimpleViewAlbumSerializer, ViewTrackSerializer, CreateTrackSerializer
from music_api.tests.utils import remove_test_media_dir

User = get_user_model()


class GenreSerializerTestCase(TestCase):

    def setUp(self):
        self.genre1 = Genre.objects.create(title='jazz')
        self.genre2 = Genre.objects.create(title='electro')

    def test_all_fields(self):
        data = GenreSerializer([self.genre1, self.genre2], many=True).data
        expected_data = [
            {
                'id': self.genre1.id,
                'title': 'jazz'
            },
            {
                'id': self.genre2.id,
                'title': 'electro'
            }
        ]
        self.assertEqual(data, expected_data)


class MusicAuthorSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user')

    def test_all_fields(self):
        data = MusicAuthorSerializer(self.user).data
        expected_data = {
            'id': self.user.id,
            'username': 'user'
        }
        self.assertEqual(data, expected_data)


class AlbumSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user')
        self.genre1 = Genre.objects.create(title='jazz')
        self.genre2 = Genre.objects.create(title='electro')

    def test_create(self):
        data = {
            'title': 'Test title',
            'author': self.user.id,
            'genres': [self.genre1.id, self.genre2.id],
        }
        self.assertTrue(CreateAlbumSerializer(data=data).is_valid())

    def test_view(self):
        album = Album.objects.create(title='Album', author=self.user)
        album.genres.add(self.genre1, self.genre2)
        data = ViewAlbumSerializer(album).data
        expected_data = {
            'id': album.id,
            'title': 'Album',
            'author': {
                'id': self.user.id,
                'username': 'user'
            },
            'genres': [
                {
                    'id': self.genre1.id,
                    'title': 'jazz'
                },
                {
                    'id': self.genre2.id,
                    'title': 'electro'
                }
            ],
            'date_added': str(album.date_added),
            'cover': None,
            'plays_count': 0
        }
        self.assertEqual(data, expected_data)

    def test_simple_view(self):
        album = Album.objects.create(title='Album', author=self.user)
        data = SimpleViewAlbumSerializer(album).data
        expected_data = {
            'id': album.id,
            'title': 'Album'
        }
        self.assertEqual(data, expected_data)


@override_settings(MEDIA_ROOT=settings.TEST_MEDIA_ROOT)
class TrackSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user')
        self.genre1 = Genre.objects.create(title='jazz')
        self.genre2 = Genre.objects.create(title='electro')
        self.album = Album.objects.create(title='Album', author=self.user)
        self.album.genres.add(self.genre1, self.genre2)
        self.file = SimpleUploadedFile('track.mp3', b'bbb')
        self.track = Track.objects.create(
            title='Track',
            author=self.user,
            album=self.album,
            file=self.file
        )
        self.track.genres.add(self.genre1, self.genre2)

    def test_create(self):
        data = {
            'title': 'Test title',
            'genres': [self.genre1.id, self.genre2.id],
            'file': self.file
        }
        self.assertTrue(CreateTrackSerializer(data=data).is_valid())

    def test_view(self):
        data = ViewTrackSerializer(self.track).data
        expected_data = {
            'id': self.track.id,
            'title': 'Track',
            'author': {
                'id': self.user.id,
                'username': 'user'
            },
            'genres': [
                {
                    'id': self.genre1.id,
                    'title': 'jazz'
                },
                {
                    'id': self.genre2.id,
                    'title': 'electro'
                }
            ],
            'date_added': str(self.track.date_added),
            'cover': None,
            'plays_count': 0,
            'file': self.track.file.url,
            'album': {
                'id': self.album.id,
                'title': 'Album'
            },
            'downloads_count': 0
        }
        self.assertEqual(data, expected_data)

    def tearDown(self):
        remove_test_media_dir()