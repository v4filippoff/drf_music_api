from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    1) Разрешаем пользователю извлекать ресурс, если http метод является безопасным (GET, HEAD, OPTIONS)
    2) Если http запрос на изменение ресурса (PUT, PATCH, DELETE), то проверяем принадлежность ресурса пользователю
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and request.user == obj
        )


class IsUrlOwnerOrReadOnly(BasePermission):
    """
    Проверяем запрашивает ли текущий пользователь ресурс со своим id
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.id == view.kwargs['user_id']
        )