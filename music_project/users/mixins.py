from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.models import SocialLink
from users.permissions import IsSocialLinksOwnerOrReadOnly

User = get_user_model()


class UserItemsMixin:
    """
    Базовый миксин для получения списка many-объектов пользователя
    """
    item_model = None
    owner_model_field = None
    owner_url_kwarg = None

    def get_queryset(self):
        owner = self.get_owner()
        return self.item_model.objects.filter(**{self.owner_model_field: owner})

    def get_owner(self):
        owner_id = self.kwargs.get(self.owner_url_kwarg)
        owner = get_object_or_404(User, id=owner_id)
        return owner


class SocialLinksMixin(UserItemsMixin):
    """
    Определяем поля для получения ссылок на соц.сети пользователя
    """
    permission_classes = [IsSocialLinksOwnerOrReadOnly]

    item_model = SocialLink
    owner_model_field = 'user'
    owner_url_kwarg = 'user_id'