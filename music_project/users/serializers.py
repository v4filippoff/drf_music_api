from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'description',
            'country',
            'avatar'
        ]
        extra_kwargs = {'username': {'read_only': True}}
