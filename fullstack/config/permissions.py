from rest_framework import permissions

from cart.cart import Cart


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
        cart = Cart(request)
        if len(cart):
            return True
        return False
