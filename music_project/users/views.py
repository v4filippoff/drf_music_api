from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

from users.serializers import UserProfileSerializer


User = get_user_model()


class UserProfileViewSet(ViewSetMixin, ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
