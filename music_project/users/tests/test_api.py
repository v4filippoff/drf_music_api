from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.serializers import UserProfileSerializer

User = get_user_model()


class UserProfileApiTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='test_user1',
            description='Test description1',
            country='Russia'
        )
        self.user2 = User.objects.create(
            username='test_user2',
            description='Test description2',
            country='Usa'
        )
        self.user3 = User.objects.create(
            username='test_user3',
            description='Test description3',
            country='Russia'
        )

    def test_get_list(self):
        url = reverse('users-list')
        response = self.client.get(url)
        users = User.objects.all()
        serializer_data = UserProfileSerializer(users, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_filter(self):
        url = reverse('users-list')
        response = self.client.get(url, data={'country': 'USA'})
        users = User.objects.filter(country='USA')
        serializer_data = UserProfileSerializer(users, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_search(self):
        url = reverse('users-list')
        response = self.client.get(url, data={'search': 'test_user1'})
        users = User.objects.filter(username='test_user1')
        serializer_data = UserProfileSerializer(users, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_detail(self):
        url = reverse('users-detail', args=(self.user1.id,))
        response = self.client.get(url)
        user = User.objects.filter(id=self.user1.id).get()
        serializer_data = UserProfileSerializer(user).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, serializer_data)

    def test_update(self):
        url = reverse('users-detail', args=(self.user1.id,))
        data = {
            'username': self.user1.username,
            'description': 'New description',
            'country': self.user1.country
        }
        self.client.force_login(self.user1)
        response = self.client.put(url, data=data, content_type='application/json')
        self.user1.refresh_from_db()

        self.assertEqual(data['description'], self.user1.description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('users-detail', args=(self.user1.id,))
        self.client.force_login(self.user1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_update_not_owner(self):
        url = reverse('users-detail', args=(self.user1.id,))
        data = {
            'username': self.user1.username,
            'description': 'New description',
            'country': self.user1.country
        }
        self.client.force_login(self.user2)
        response = self.client.put(url, data=data, content_type='application/json')
        self.user1.refresh_from_db()

        self.assertEqual(self.user1.description, 'Test description1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_owner(self):
        url = reverse('users-detail', args=(self.user1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
