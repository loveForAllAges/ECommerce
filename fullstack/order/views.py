from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Order, Product, OrderItem, Address
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import AddressForm, OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from order.context_processors import cart


class CartListView(ListView):
    template_name = 'usage/cartList.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Order.objects.filter(customer=user, status=1)
        else:
            queryset = ''

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


class OrderListView(UserPassesTestMixin, ListView):
    template_name = 'adm/orderList.html'

    def get_queryset(self):
        queryset = Order.objects.filter(status=1)

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class CheckoutView(UserPassesTestMixin, View):
    template_name = 'usage/checkout.html'

    def get(self, request):
        context = {
            'order_form': OrderForm,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        pass

    def test_func(self):
        if not cart(self.request)['items']:
            raise Http404
        return True


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'usage/addressCreate.html'
    success_url = reverse_lazy('account')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.customer = self.request.user
        return super().form_valid(form)
    

class AddressUpdateView(UserPassesTestMixin, UpdateView):
    model = Address
    fields = ('city', 'address', 'zipcode')
    template_name = 'usage/addressCreate.html'
    success_url = reverse_lazy('account')

    def test_func(self):
        pk = self.kwargs.get('pk')
        item = Address.objects.get(id=pk)
        user = self.request.user
        if not user.is_authenticated or not item.customer == user:
            raise Http404
        return True


class AddressDeleteView(UserPassesTestMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('account')
    template_name = ''

    def test_func(self):
        pk = self.kwargs.get('pk')
        item = Address.objects.get(id=pk)
        user = self.request.user
        if not self.request.user.is_authenticated or not item.customer == user:
            raise Http404
        return True
    