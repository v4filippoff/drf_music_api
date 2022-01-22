from django.contrib import admin
from users.models import User, SocialLink, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'description',
        'country',
        'date_joined',
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'link',
    )


@admin.register(Subscription)
class SubscriptionLinkAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
