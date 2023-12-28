from functools import wraps

from product.utils import get_main_categories
from cart.utils import get_serialized_cart
from .utils import get_deliveries


def cart_and_categories_and_deliveries(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        combined_data = {
            'cart': get_serialized_cart(args[0]),
            'categories': get_main_categories(args[0]),
            'deliveries': get_deliveries(),
        }

        response.data.update(combined_data)
        return response
    return _wrapped_view
