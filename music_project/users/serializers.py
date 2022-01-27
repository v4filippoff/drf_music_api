from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from users.models import SocialLink, Subscription

User = get_user_model()


class SocialLinkSerializer(ModelSerializer):
    class Meta:
        model = SocialLink
        fields = [
            'id',
            'link'
        ]


class UserProfileSerializer(ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'description',
            'country',
            'avatar',
            'social_links'
        ]


class SubscriptionSerializer(ModelSerializer):
    author_name = SerializerMethodField('get_author_name')
    url = CharField(source='author.get_absolute_url', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'author',
            'author_name',
            'url'
        ]

    def get_author_name(self, obj):
        return obj.author.username


class SubscriberSerializer(ModelSerializer):
    user_name = SerializerMethodField('get_user_name')
    url = CharField(source='user.get_absolute_url', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'user_name',
            'url'
        ]

    def get_user_name(self, obj):
        return obj.user.username