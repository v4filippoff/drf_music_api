from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, GenericViewSet

from users.mixins import UserItemsMixin, SocialLinksMixin
from users.models import Subscription
from users.permissions import IsProfileOwnerOrReadOnly, IsNotSubscribersOwnerOrReadOnly
from users.serializers import UserProfileSerializer, SocialLinkSerializer, SubscriberSerializer

User = get_user_model()


class UserProfileViewSet(ViewSetMixin, ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.prefetch_related('social_links')
    serializer_class = UserProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['country']
    search_fields = ['username']


class ListCreateSocialLinkView(SocialLinksMixin, ViewSetMixin, ListCreateAPIView):
    serializer_class = SocialLinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateDestroySocialLinkView(SocialLinksMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SocialLinkSerializer
    lookup_url_kwarg = 'link_id'


class ListCreateDestroySubscriptionView(UserItemsMixin, ViewSetMixin, DestroyModelMixin, ListCreateAPIView):
    serializer_class = SubscriberSerializer
    permission_classes = [IsNotSubscribersOwnerOrReadOnly]

    item_model = Subscription
    owner_model_field = 'author'
    owner_url_kwarg = 'author_id'

    def create(self, request, *args, **kwargs):
        author = self.get_owner()
        if not Subscription.objects.filter(author=author, user=request.user).exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({'detail': 'Object already exists'}, status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer):
        author = self.get_owner()
        serializer.save(author=author, user=self.request.user)

    def get_object(self):
        return get_object_or_404(Subscription, author=self.get_owner(), user=self.request.user)
