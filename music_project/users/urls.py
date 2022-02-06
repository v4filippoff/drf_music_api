from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import (UserProfileViewSet, SocialLinkListCreateView, SocialLinkUpdateDestroyView,
                         FollowListCreateView, FollowDestroyView, FollowersListView)

router = SimpleRouter()
router.register('users', UserProfileViewSet)

urlpatterns = [
    path('users/<int:user_id>/social-links/', SocialLinkListCreateView.as_view(), name='social-link-list'),
    path('users/<int:user_id>/social-links/<int:link_id>/', SocialLinkUpdateDestroyView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='social-link-detail'
    ),
    path('users/<int:user_id>/following/', FollowListCreateView.as_view(), name='following-list'),
    path('users/<int:user_id>/following/<int:author_id>/', FollowDestroyView.as_view(),
         name='following-detail'),

    path('users/<int:author_id>/followers/', FollowersListView.as_view(), name='follower-list'),
]

urlpatterns += router.urls
