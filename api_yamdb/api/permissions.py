from rest_framework import permissions


class IsAdminOrReadOnly1(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    message = 'Недостаточно прав для запроса'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin or request.user.is_superuser
        )
    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin or request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_moderator)


class IsAdminForTitlesOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав для запроса'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )
