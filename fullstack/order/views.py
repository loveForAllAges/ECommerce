from django.db.models.query import QuerySet
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Order
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from cart.context_processors import cart


class CartListView(ListView):
    template_name = 'usage/cartList.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Order.objects.filter(customer=user, status=1)
        else:
            queryset = ''

        return queryset


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
        data = request.POST
        address = data.get('address')
        if request.user.is_authenticated:
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            phone = request.user.phone

            order = Order.objects.get(customer=request.user, status=1)
            order.first_name = first_name
            order.last_name = last_name
            order.email = email
            order.phone = phone
        else:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            order = Order.objects.create(first_name=first_name, last_name=last_name,
                                         email=email, phone=phone)

        order.address = address
        order.status = 2
        order.save()
        return HttpResponse('OK')

    def test_func(self):
        if not cart(self.request)['items']:
            raise Http404
        return True
