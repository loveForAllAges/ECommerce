from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from .models import Order
import json
from django.http import JsonResponse


# TODO private func
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
    print([data])
    return JsonResponse('Success')
