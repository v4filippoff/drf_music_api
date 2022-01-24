from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwnerOrReadOnly(BasePermission):
    """
    1) Разрешаем пользователю извлекать ресурс с профилем, если http метод является безопасным (GET, HEAD, OPTIONS)
    2) Если http запрос на изменение ресурса (PUT, PATCH, DELETE), то проверяем принадлежность профиля пользователю
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and
            request.user == obj
        )


class IsSocialLinksOwnerOrReadOnly(BasePermission):
    """
    Проверка проходит, если текущий пользователь запрашивает ресурс со своим id
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and
            request.user.id == view.kwargs['user_id']
        )


class IsNotSubscribersOwnerOrReadOnly(BasePermission):
    """
    Проверка проходит если текущий пользователь запрашивает ресурс НЕ со своим id
    (это необходимо для того, чтобы подписываться на пользователя могли все, кроме него самого)
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and
            request.user.id != view.kwargs['author_id']
        )