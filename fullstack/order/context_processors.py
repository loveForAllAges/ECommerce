
import json
from .models import *
from django.shortcuts import HttpResponse


def parseCookies(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))

    items = []
    order = {
        'number_of_items_in_cart': 0,
        'total_price': 0
    }

    for i in list(cart.keys()):
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
        except Exception as error:
            del cart[i]

    return {
        'order': order,
        'items': items,
    }


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, status=1)
        items = order.orderitem_set.all()
    else:
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
