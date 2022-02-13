from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User, SocialLink, Follow


# Форма для переопределения дефолтной формы создания юзера в админке
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


# Форма для переопределения дефолтной формы изменения юзера в админке
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


# Переопределяем дефолтный класс админки юзера, указывая кастомные формы (см. выше) и
# дополнительные поля из нашего кастомного юзера
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (
                'description',
                'country',
                'avatar',
            )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (
            'email',
        )}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'link',
    )
    list_display_links = ('link',)


@admin.register(Follow)
class FollowLinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )