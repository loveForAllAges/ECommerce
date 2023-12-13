from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 12

    def get_paginated_response(self):
        return {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }