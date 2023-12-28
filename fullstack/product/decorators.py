from functools import wraps

from .utils import get_main_categories, get_filters, get_queries
from cart.utils import get_serialized_cart


def cart_and_categories(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        combined_data = {
            'cart': get_serialized_cart(args[0]),
            'categories': get_main_categories(args[0]),
        }

        response.data.update(combined_data)
        return response
    return _wrapped_view


def cart_and_categories_and_filters_and_queries(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        combined_data = {
            'cart': get_serialized_cart(args[0]),
            'categories': get_main_categories(args[0]),
            'filters': get_filters(),
            'queries': get_queries(args[0]),
        }

        response.data.update(combined_data)
        return response
    return _wrapped_view
