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


class SocialLink(models.Model):
    """
    Модель ссылок на соц.сети пользователя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField('User social link')

    def __str__(self):
        return '{0}: {1}'.format(self.user.username, self.link)


class Subscription(models.Model):
    """
    Модель подписки на автора
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return '{0} is subscribed on {1}'.format(self.user, self.author)
