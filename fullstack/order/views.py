from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from .models import Order


# TODO private func
class CartListView(ListView):
    template_name = 'usage/cartList.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user, status=1)
        return queryset


# TODO private func
class OrderListView(ListView):
    template_name = 'usage/orderList.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).exclude(status=1)
        return queryset

