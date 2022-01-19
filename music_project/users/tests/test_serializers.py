from io import BytesIO
import os
import shutil

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from users.models import User
from users.serializers import UserSerializer


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

        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)
        self.user1.avatar = SimpleUploadedFile('image.jpg', image.getvalue())
        self.user1.save()

    def test_all_fields(self):
        data = UserSerializer([self.user1, self.user2], many=True).data
        expected_data = [
            {
                'id': self.user1.id,
                'username': 'TestUser',
                'description': 'Test Description',
                'country': 'Russia',
                'avatar': self.user1.avatar.url
            },
            {
                'id': self.user2.id,
                'username': 'TestUser2',
                'description': 'Test Description2',
                'country': 'USA',
                'avatar': None
            }
        ]
        self.assertEqual(data, expected_data)

    def tearDown(self):
        """
        Удаляем медиа-директорию тестового пользователя
        """
        dirname_with_image = os.path.dirname(self.user1.avatar.path)
        shutil.rmtree(dirname_with_image)
