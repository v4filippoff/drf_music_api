from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.mixins import UserItemsMixin
from users.models import Subscription, SocialLink
from users.permissions import IsProfileOwnerOrReadOnly, IsUrlOwnerOrReadOnly
from users.serializers import UserProfileSerializer, SocialLinkSerializer, SubscriptionSerializer, SubscriberSerializer

User = get_user_model()


class UserProfileViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = User.objects.prefetch_related('social_links')
    serializer_class = UserProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['country']
    search_fields = ['username']


class ListCreateSocialLinkView(UserItemsMixin, ListCreateAPIView):
    serializer_class = SocialLinkSerializer
    permission_classes = [IsUrlOwnerOrReadOnly]
    item_model = SocialLink

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateDestroySocialLinkView(UserItemsMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SocialLinkSerializer
    lookup_url_kwarg = 'link_id'
    permission_classes = [IsUrlOwnerOrReadOnly]
    item_model = SocialLink


class ListCreateSubscriptionView(UserItemsMixin, ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsUrlOwnerOrReadOnly]
    item_model = Subscription

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data['author']

        if not Subscription.objects.filter(user=request.user, author=author).exists():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'Object already exists'}, status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer):
        author = serializer.validated_data['author']
        serializer.save(user=self.request.user, author=author)


class DestroySubscriptionView(UserItemsMixin, DestroyAPIView):
    permission_classes = [IsUrlOwnerOrReadOnly]
    lookup_field = 'author_id'
    item_model = Subscription


class ListSubscriberView(UserItemsMixin, ListAPIView):
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    item_model = Subscription
    owner_model_field = 'author'
    owner_url_kwarg = 'author_id'
