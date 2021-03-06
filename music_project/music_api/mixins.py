from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.serializers import BaseSerializer


class SerializerSetMixin:
    """
    Миксин для указания набора сериализаторов для чтения объектов и изменения/создания
    """
    # 'read' - сериализатор для read only
    # 'write' - сериализатор для write only
    serializer_set = {
        'read': None,
        'write': None
    }

    def get_serializer_class(self):
        assert self.serializer_set['read'] and self.serializer_set['write'], (
            'Необходимо указать сериализаторы для просмотра объекта (read)'
            ' и его изменения/создания (write) атрибуту serializer_set'
        )
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return self.serializer_set['read']
        return self.serializer_set['write']


class MusicEntityFilterBackendsMixin:
    """
    Дефолтные фильтры для треков и альбомов
    """
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['date_added', 'plays_count']