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


class IsUrlOwnerOrReadOnly(BasePermission):
    """
    Проверка проходит, если текущий пользователь запрашивает ресурс со своим id
    """
    def has_permission(self, request, view):
        required_attr = 'owner_url_kwarg'
        if not hasattr(view, required_attr):
            raise AttributeError(
                f"'{view.get_view_name()}' view has no attribute '{required_attr}'"
            )

        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and
            request.user.id == view.kwargs.get(getattr(view, required_attr))
        )
