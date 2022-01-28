from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import (UserProfileViewSet, ListCreateSocialLinkView, UpdateDestroySocialLinkView,
                         ListCreateFollowView, DestroyFollowView, ListFollowersView)

router = SimpleRouter()
router.register('users', UserProfileViewSet)

urlpatterns = [
    path('users/<int:user_id>/social-links/', ListCreateSocialLinkView.as_view(), name='social-link-list'),
    path('users/<int:user_id>/social-links/<int:link_id>/', UpdateDestroySocialLinkView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='social-link-detail'
    ),
    path('users/<int:user_id>/following/', ListCreateFollowView.as_view(), name='following-list'),
    path('users/<int:user_id>/following/<int:author_id>/', DestroyFollowView.as_view(),
         name='following-detail'),

    path('users/<int:author_id>/followers/', ListFollowersView.as_view(), name='follower-list'),
]

urlpatterns += router.urls
