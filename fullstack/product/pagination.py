from rest_framework.pagination import CursorPagination, Cursor
from rest_framework.reverse import reverse


class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 2

    def get_paginated_response(self, request=None):
        if request:
            self.base_url = request.build_absolute_uri(reverse('more_products_api'))
        return self.get_next_link()
