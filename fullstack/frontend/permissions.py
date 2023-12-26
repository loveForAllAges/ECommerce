from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if self.request.user.is_authenticated:
            raise Http404
        return True
