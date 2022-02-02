from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User, SocialLink, Follow
from users.serializers import UserProfileSerializer, FollowingSerializer, FollowerSerializer
from users.tests.utils import delete_avatars


class UserSerializerTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='TestUser',
            description='Test Description',
            country='Russia',
            avatar=SimpleUploadedFile('avatar.jpg', b'aaa')
        )
        self.user2 = User.objects.create(
            username='TestUser2',
            description='Test Description2',
            country='USA'
        )

        self.social_link1 = SocialLink.objects.create(user=self.user1, link='https://test.com')
        self.social_link2 = SocialLink.objects.create(user=self.user1, link='https://facebook.com')
        self.social_link3 = SocialLink.objects.create(user=self.user2, link='https://youtube.com')

    def test_all_fields(self):
        data = UserProfileSerializer([self.user1, self.user2], many=True).data
        expected_data = [
            {
                'id': self.user1.id,
                'username': 'TestUser',
                'description': 'Test Description',
                'country': 'Russia',
                'avatar': self.user1.avatar.url,
                'social_links': [
                    {
                        'id': self.social_link1.id,
                        'link': 'https://test.com'
                    },
                    {
                        'id': self.social_link2.id,
                        'link': 'https://facebook.com'
                    }
                ]
            },
            {
                'id': self.user2.id,
                'username': 'TestUser2',
                'description': 'Test Description2',
                'country': 'USA',
                'avatar': None,
                'social_links': [
                    {
                        'id': self.social_link3.id,
                        'link': 'https://youtube.com'
                    }
                ]
            }
        ]
        self.assertEqual(data, expected_data)

    def tearDown(self):
        delete_avatars(self.user1.avatar)


class FollowingSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='TestUser',
            description='Test Description',
            country='USA'
        )
        self.author1 = User.objects.create(
            username='TestAuthor1',
            description='Test Description',
            country='Russia'
        )
        self.author2 = User.objects.create(
            username='TestAuthor2',
            description='Test Description',
            country='Russia'
        )
        self.sub1 = Follow.objects.create(user=self.user, author=self.author1)
        self.sub2 = Follow.objects.create(user=self.user, author=self.author2)

    def test_all_fields(self):
        data = FollowingSerializer([self.sub1, self.sub2], many=True).data
        expected_data = [
            {
                'author': self.author1.id,
                'author_name': 'TestAuthor1',
                'url': f'/api/users/{self.author1.id}/'
            },
            {
                'author': self.author2.id,
                'author_name': 'TestAuthor2',
                'url': f'/api/users/{self.author2.id}/'
            }
        ]
        self.assertEqual(data, expected_data)


class FollowerSerializerTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create(
            username='TestAuthor',
            description='Test Description',
            country='Russia'
        )
        self.user1 = User.objects.create(
            username='TestUser1',
            description='Test Description1',
            country='USA'
        )
        self.user2 = User.objects.create(
            username='TestUser2',
            description='Test Description2',
            country='Russia'
        )
        self.sub1 = Follow.objects.create(user=self.user1, author=self.author)
        self.sub2 = Follow.objects.create(user=self.user2, author=self.author)

    def test_all_fields(self):
        data = FollowerSerializer([self.sub1, self.sub2], many=True).data
        expected_data = [
            {
                'user': self.user1.id,
                'user_name': self.user1.username,
                'url': f'/api/users/{self.user1.id}/'
            },
            {
                'user': self.user2.id,
                'user_name': self.user2.username,
                'url': f'/api/users/{self.user2.id}/'
            }
        ]
        self.assertEqual(data, expected_data)