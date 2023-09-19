
import json
from .models import *


def parseCookies(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'number_of_items_in_cart': 0,
        'total_price': 0
    }

    print('='*10, cart, '='*10)

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['total_price'] += total
            order['number_of_items_in_cart'] += cart[i]['quantity']

            item = {
                'product': product,
                'quantity': cart[i]['quantity'],
                'get_total_price': total,
            }
            items.append(item)
        except:
            pass

    return {
        'order': order,
        'items': items,
    }


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, status=1)
        items = order.orderitem_set.all()
    else:
        print('NOT AUTH')
        cookieData = parseCookies(request)
        order = cookieData['order']
        items = cookieData['items']
    return {
        'order': order,
        'items': items,
    }


# def guestOrder(request, data):
#     print('User is not logged in')

#     name = data['form']['name']
#     email = data['form']['email']
#     cookieData = cookieCart(request)
#     items = cookieData['items']
#     customer, created = Customer.objects.get_or_create(
#         email=email,
#     )
#     customer.name = name
#     customer.save()

#     order = Order.objects.create(
#         customer=customer,
#         complete=False,
#     )

#     for item in items:
#         product = Product.objects.get(id=item['product']['id'])
#         orderItem = OrderItem.objects.create(
#             product=product,
#             order=order,
#             quantity=item['quantity'],
#         )
#     return customer, order
