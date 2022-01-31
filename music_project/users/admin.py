from django.contrib import admin
from users.models import User, SocialLink, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'description',
        'country',
        'date_joined',
    )
    list_display_links = ('username',)


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