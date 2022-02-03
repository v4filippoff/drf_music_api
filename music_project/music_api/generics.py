from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from music_api.permissions import IsAuthorOrReadOnly


class MusicEntityViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]

    # 'read' - сериализатор для read only
    # 'write' - сериализатор для write only
    serializer_set = {
        'read': None,
        'write': None
    }

    def get_serializer_class(self):
        assert (isinstance(self.serializer_set['read'], BaseSerializer.__class__) and
                isinstance(self.serializer_set['write'], BaseSerializer.__class__)), (
            'Необходимо указать сериализаторы для просмотра объекта (read)'
            ' и его изменения (write) атрибуту serializer_set'
        )
        if self.request.method == 'GET':
            return self.serializer_set['read']
        return self.serializer_set['write']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)