from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.reverse import reverse


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 36

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 36

    def get_paginated_response(self, request=None):
        if request:
            self.base_url = request.build_absolute_uri(reverse('more_products_api'))
        return self.get_next_link()
