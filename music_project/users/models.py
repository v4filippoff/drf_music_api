from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from users.services import get_avatar_upload_path


class User(AbstractUser):
    """
    Модель пользователя
    """
    description = models.CharField('User description', max_length=2000, blank=True, null=True)
    country = models.CharField('Country', max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        'User avatar',
        upload_to=get_avatar_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    def get_absolute_url(self):
        return reverse('user-detail', args=(self.pk,))


class SocialLink(models.Model):
    """
    Модель ссылок на соц.сети пользователя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField('User social link')

    def __str__(self):
        return '{0}: {1}'.format(self.user.username, self.link)


class Follow(models.Model):
    """
    Модель подписки на автора
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return '{0} is followed on {1}'.format(self.user, self.author)
