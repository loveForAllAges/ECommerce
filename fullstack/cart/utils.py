import json
from order.models import Order
from product.models import Product


def cookieCart(request):
    cart = json.loads(request.COOKIES.get('cart'))
    items = []
    
    order = {
        'get_cart_items': 0,
        'get_cart_total': 0
    }

    for i in cart:
        print(i)
    #     order['get_cart_items'] += cart[i]['quantity']
    #     product = Product.objects.get(id=i)
    #     order['get_cart_total'] += product.price * cart[i]['quantity']
        
    #     item = {
    #         'product': {
    #             'id': product.id,
    #             'name': product.name,
    #             'product': product.price,
    #         },
    #         'quantity': cart[i]['quantity'],
    #         'get_total_price': product.price * cart[i]['quantity']
    #     }
    #     items.append(item)

    return {'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        order = Order.objects.get_or_create(customer=request.user, is_done=False)
        items = order.orderitem_set.all()
    else:
        data = cookieCart(request)
        order = data['order']
        items = data['items']
    return {'order': order, 'items': items}
