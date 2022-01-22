from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.viewsets import ViewSetMixin

from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserProfileSerializer

User = get_user_model()


class UserProfileViewSet(ViewSetMixin, ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['country']
    search_fields = ['username']