from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404

from cart.utils import cart_not_empty


class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if self.request.user.is_authenticated:
            raise Http404
        return True


class CartNotEmptyMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if not cart_not_empty(self.request):
            raise Http404
        return True
