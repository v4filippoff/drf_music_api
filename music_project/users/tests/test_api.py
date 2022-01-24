from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import SocialLink, Subscription
from users.serializers import UserProfileSerializer, SocialLinkSerializer, SubscriberSerializer

User = get_user_model()


class BaseUserApiTestCase(TestCase):

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
        self.social_link1 = SocialLink.objects.create(user=self.user1, link='https://test.com')
        self.social_link2 = SocialLink.objects.create(user=self.user1, link='https://facebook.com')
        self.social_link3 = SocialLink.objects.create(user=self.user2, link='https://youtube.com')

        self.sub1 = Subscription.objects.create(user=self.user2, author=self.user1)
        self.sub2 = Subscription.objects.create(user=self.user3, author=self.user1)


class UserProfileApiTestCase(BaseUserApiTestCase):

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


class SocialLinksApiTestCase(BaseUserApiTestCase):

    def test_get_list(self):
        url = reverse('social-link-list', args=(self.user1.id,))
        response = self.client.get(url)
        social_links = SocialLink.objects.filter(user=self.user1)
        serializer_data = SocialLinkSerializer(social_links, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_create(self):
        url = reverse('social-link-list', args=(self.user1.id,))
        data = {
            'link': 'https://github.com/user1'
        }
        self.client.force_login(self.user1)
        response = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user1.social_links.count(), 3)

    def test_update(self):
        url = reverse('social-link-detail', args=(self.user1.id, self.social_link1.id))
        data = {
            'link': 'https://changed-link.com'
        }
        self.client.force_login(self.user1)
        response = self.client.put(url, data=data, content_type='application/json')
        self.social_link1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['link'], self.social_link1.link)

    def test_delete(self):
        url = reverse('social-link-detail', args=(self.user1.id, self.social_link1.id))
        self.client.force_login(self.user1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SocialLink.objects.count(), 2)
        self.assertFalse(SocialLink.objects.filter(id=self.social_link1.id).exists())

    def test_update_not_owner(self):
        url = reverse('social-link-detail', args=(self.user1.id, self.social_link1.id))
        data = {
            'link': 'https://changed-link.com'
        }
        self.client.force_login(self.user2)
        response = self.client.put(url, data=data, content_type='application/json')
        self.social_link1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.social_link1.link, 'https://test.com')

    def test_user_404_not_found(self):
        url = reverse('social-link-list', args=(10000,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionsApiTestCase(BaseUserApiTestCase):

    def test_get_list(self):
        url = reverse('sub-list', args=(self.user1.id,))
        response = self.client.get(url)
        subs = Subscription.objects.filter(author=self.user1)
        serializer_data = SubscriberSerializer(subs, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_subscribe(self):
        url = reverse('sub-list', args=(self.user1.id,))
        user4 = User.objects.create(username='user4')
        self.client.force_login(user4)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user1.subscribers.count(), 3)
        self.assertTrue(Subscription.objects.filter(author=self.user1, user=user4).exists())

    def test_unsubscribe(self):
        url = reverse('sub-list', args=(self.user1.id,))
        self.client.force_login(self.user3)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user1.subscribers.count(), 1)
        self.assertFalse(Subscription.objects.filter(author=self.user1, user=self.user3).exists())

    def test_double_subscribe(self):
        url = reverse('sub-list', args=(self.user1.id,))
        self.client.force_login(self.user3)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(self.user1.subscribers.count(), 2)

    def test_unsubscribe_before_subscription(self):
        url = reverse('sub-list', args=(self.user1.id,))
        user4 = User.objects.create(username='user4')
        self.client.force_login(user4)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.user1.subscribers.count(), 2)

    def test_subscribe_by_author(self):
        url = reverse('sub-list', args=(self.user1.id,))
        self.client.force_login(self.user1)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user1.subscribers.count(), 2)
        self.assertFalse(Subscription.objects.filter(author=self.user1, user=self.user1).exists())