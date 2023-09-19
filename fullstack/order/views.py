from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from .models import Order, Product, OrderItem
import json
from django.http import JsonResponse
from django.contrib import messages


class CartListView(ListView):
    template_name = 'usage/cartList.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Order.objects.filter(customer=user, status=1)
        else:
            queryset = ''

        return queryset


# TODO private func
class OrderListView(ListView):
    template_name = 'usage/orderList.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).exclude(status=1)
        return queryset


def cart_update(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=request.user, status=1)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'plus':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
    elif action == 'minus':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
    elif action == 'remove':
        orderItem.delete()

    messages.add_message(request, messages.INFO, 'Корзина обновлена')

    return JsonResponse('Success', safe=False)
