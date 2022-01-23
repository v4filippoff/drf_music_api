from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from users.models import SocialLink

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
