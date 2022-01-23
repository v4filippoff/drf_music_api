from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ViewSetMixin, GenericViewSet

from users.mixins import UserSocialLinksMixin
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserProfileSerializer, SocialLinkSerializer

User = get_user_model()


class UserProfileViewSet(ViewSetMixin, ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['country']
    search_fields = ['username']


class ListCreateSocialLinkView(UserSocialLinksMixin, ViewSetMixin, ListCreateAPIView):
    serializer_class = SocialLinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateDestroySocialLink(UserSocialLinksMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SocialLinkSerializer
    lookup_url_kwarg = 'link_id'

