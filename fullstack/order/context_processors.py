
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
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])
        order['total_price'] += total
        order['number_of_items_in_cart'] += cart[i]['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'photos': product.productphoto_set.all(),
            },
            'quantity': cart[i]['quantity'],
            'get_total_price': total,
        }
        items.append(item)

    return {
        'order': order,
        'items': items,
    }


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, status=1)
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
