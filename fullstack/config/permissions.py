from rest_framework import permissions

from cart.models import Cart
from cart.utils import cart_not_empty


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser) or
            request.method in permissions.SAFE_METHODS
        )


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated or request.method == 'POST'
        )


class CartExists(permissions.BasePermission):
    def has_permission(self, request, view):
        if cart_not_empty(request):
            return True

