from .cart import Cart


def cart(request):
    cart = Cart(request)
    return {
        'items': cart.get_items, 
        'total_quantity': len(cart), 
        'total_price': cart.get_total_price
    }
