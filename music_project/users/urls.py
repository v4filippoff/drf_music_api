from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import UserProfileViewSet, ListCreateSocialLinkView, UpdateDestroySocialLink

router = SimpleRouter()
router.register('users', UserProfileViewSet, basename='users')

urlpatterns = [
    path('users/<int:user_id>/social-links/<int:link_id>/', UpdateDestroySocialLink.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='social-link-detail'
    ),
    path('users/<int:user_id>/social-links/', ListCreateSocialLinkView.as_view(
        {'get': 'list', 'post': 'create'}), name='social-link-list'
    ),
]

urlpatterns += router.urls
