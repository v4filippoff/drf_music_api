from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models

from .services import get_avatar_upload_path


class User(AbstractUser):
    """
    Модель пользователя
    """

    slug = AutoSlugField(populate_from='username')
    description = models.CharField('User description', max_length=2000, blank=True)
    country = models.CharField('Country', max_length=50, blank=True)
    avatar = models.ImageField(
        'User avatar',
        upload_to=get_avatar_upload_path,
        blank=True,
        null=True
    )