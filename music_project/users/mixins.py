from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.models import SocialLink
from users.permissions import IsUrlOwnerOrReadOnly

User = get_user_model()

class UserSocialLinksMixin:
    """
    Получаем список ссылок на соц.сети, отфильтровав по user_id полю
    """
    permission_classes = [IsUrlOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        return SocialLink.objects.filter(user=user)