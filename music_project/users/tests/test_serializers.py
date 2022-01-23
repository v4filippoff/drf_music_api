from io import BytesIO
import os
import shutil

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from users.models import User, SocialLink
from users.serializers import UserProfileSerializer


class UserSerializerTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='TestUser',
            description='Test Description',
            country='Russia'
        )
        self.user2 = User.objects.create(
            username='TestUser2',
            description='Test Description2',
            country='USA'
        )

        self.social_link1 = SocialLink.objects.create(user=self.user1, link='https://test.com')
        self.social_link2 = SocialLink.objects.create(user=self.user1, link='https://facebook.com')
        self.social_link3 = SocialLink.objects.create(user=self.user2, link='https://youtube.com')

        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)
        self.user1.avatar = SimpleUploadedFile('image.jpg', image.getvalue())
        self.user1.save()

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
        """
        Удаляем медиа-директорию тестового пользователя
        """
        dirname_with_image = os.path.dirname(self.user1.avatar.path)
        shutil.rmtree(dirname_with_image)
