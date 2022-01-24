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


class SubscriberSerializer(ModelSerializer):
    subscription_id = SerializerMethodField('get_subscription_id')
    username = SerializerMethodField('get_username')
    url = CharField(source='user.get_absolute_url', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'subscription_id',
            'username',
            'url'
        ]

    def get_subscription_id(self, obj):
        return obj.id

    def get_username(self, obj):
        return obj.user.username