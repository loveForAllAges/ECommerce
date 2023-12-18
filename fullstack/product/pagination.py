from rest_framework.pagination import CursorPagination, Cursor


class CustomCursorPagination(CursorPagination):
    ordering = '-id'
    page_size = 12

    def get_paginated_response(self):
        return self.get_next_link()

    def get_next_link(self):
        # TODO ДОЛЖЕН ВОЗВРАЩАТЬ ССЫЛКУ НА ДРУГОЙ ВЬЮ
        if not self.has_next:
            return None

        if self.page and self.cursor and self.cursor.reverse and self.cursor.offset != 0:
            # If we're reversing direction and we have an offset cursor
            # then we cannot use the first position we find as a marker.
            compare = self._get_position_from_instance(self.page[-1], self.ordering)
        else:
            compare = self.next_position
        offset = 0

        has_item_with_unique_position = False
        for item in reversed(self.page):
            position = self._get_position_from_instance(item, self.ordering)
            if position != compare:
                # The item in this position and the item following it
                # have different positions. We can use this position as
                # our marker.
                has_item_with_unique_position = True
                break

            # The item in this position has the same position as the item
            # following it, we can't use it as a marker position, so increment
            # the offset and keep seeking to the previous item.
            compare = position
            offset += 1

        if self.page and not has_item_with_unique_position:
            # There were no unique positions in the page.
            if not self.has_previous:
                # We are on the first page.
                # Our cursor will have an offset equal to the page size,
                # but no position to filter against yet.
                offset = self.page_size
                position = None
            elif self.cursor.reverse:
                # The change in direction will introduce a paging artifact,
                # where we end up skipping forward a few extra items.
                offset = 0
                position = self.previous_position
            else:
                # Use the position from the existing cursor and increment
                # it's offset by the page size.
                offset = self.cursor.offset + self.page_size
                position = self.previous_position

        if not self.page:
            position = self.next_position

        cursor = Cursor(offset=offset, reverse=False, position=position)
        return self.encode_cursor(cursor)
