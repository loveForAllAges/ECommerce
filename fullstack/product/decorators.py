from functools import wraps

from rest_framework.response import Response

from .utils import get_main_categories
from cart.utils import get_cart


def cart_and_categories(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        combined_data = {
            'cart': get_cart(args[0]),
            'categories': get_main_categories(args[0]),
        }

        response.data.update(combined_data)
        return response
    return _wrapped_view
