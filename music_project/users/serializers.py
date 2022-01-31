from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from users.models import SocialLink, Follow

User = get_user_model()


class SocialLinkSerializer(ModelSerializer):
    """
    Сериализатор для пользловательских ссылок на соц.сети
    """
    class Meta:
        model = SocialLink
        fields = [
            'id',
            'link'
        ]


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для профиля пользователя
    """
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
        extra_kwargs = {'username': {'read_only': True}}


class FollowingSerializer(ModelSerializer):
    """
    Сериализатор для собственных подписок пользователя
    """
    author_name = SerializerMethodField('get_author_name')
    url = CharField(source='author.get_absolute_url', read_only=True)

    class Meta:
        model = Follow
        fields = [
            'author',
            'author_name',
            'url'
        ]

    def get_author_name(self, obj):
        return obj.author.username


class FollowerSerializer(ModelSerializer):
    """
    Сериализатор для подписчиков пользователя (автора)
    """
    user_name = SerializerMethodField('get_user_name')
    url = CharField(source='user.get_absolute_url', read_only=True)

    class Meta:
        model = Follow
        fields = [
            'user',
            'user_name',
            'url'
        ]

    def get_user_name(self, obj):
        return obj.user.username