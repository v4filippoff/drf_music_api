from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import (UserProfileViewSet, ListCreateSocialLinkView, UpdateDestroySocialLinkView,
                         ListCreateSubscriptionView, DestroySubscriptionView, ListSubscriberView)

router = SimpleRouter()
router.register('users', UserProfileViewSet)

urlpatterns = [
    path('users/<int:user_id>/social-links/', ListCreateSocialLinkView.as_view(), name='social-link-list'),
    path('users/<int:user_id>/social-links/<int:link_id>/', UpdateDestroySocialLinkView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='social-link-detail'
    ),
    path('users/<int:user_id>/subscriptions/', ListCreateSubscriptionView.as_view(), name='subscription-list'),
    path('users/<int:user_id>/subscriptions/<int:author_id>/', DestroySubscriptionView.as_view(),
         name='subscription-detail'),

    path('users/<int:author_id>/subscribers/', ListSubscriberView.as_view(), name='subscriber-list'),
]

urlpatterns += router.urls
