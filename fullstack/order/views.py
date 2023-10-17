from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Order, OrderItem, DeliveryType, ORDER_CHOICES
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import OrderForm, PersonForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from cart.context_processors import cart
from cart.cart import Cart
from account.models import LastUserAddress
from django.shortcuts import get_object_or_404


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'usage/orders.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).order_by('-id')
        return queryset


class OrderDetailView(DetailView):
    template_name = 'usage/orderDetail.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = [i[1] for i in ORDER_CHOICES if i[0] != 5]
        return context


class AdmOrderListView(UserPassesTestMixin, ListView):
    template_name = 'adm/orders.html'

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
            'form': OrderForm,
            'current_delivery': 2,
            'delivery_types': DeliveryType.objects.all(),
        }
        if request.user.is_authenticated:
            adr = LastUserAddress.objects.filter(customer=request.user)
            if adr:
                context['address'] = adr[0].address
                context['city'] = adr[0].city
                context['zip_code'] = adr[0].zip_code
            context['first_name'] = request.user.first_name
            context['last_name'] = request.user.last_name
            context['email'] = request.user.email
            context['phone'] = request.user.phone
            context['disabled'] = 'disabled'

        return render(request, self.template_name, context=context)

    def post(self, request):
        data = request.POST
        current_delivery = int(data.get('delivery'))
        form = None
        if request.user.is_authenticated:
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            phone = request.user.phone
            user = request.user
        else:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            user = None

            form = PersonForm(data)

        address = {
            'address': data.get('address', None), 
            'zip_code': data.get('zip_code', None), 
            'city': data.get('city', None)
        }

        if current_delivery != 1 and (not address['address'] or not address['zip_code'] or not address['city']) or (form and not form.is_valid()):
            messages.add_message(request, messages.ERROR, 'Введены некорректные данные')
            context = {
                'form': OrderForm,
                'address': address,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'delivery_types': DeliveryType.objects.all(),
                'current_delivery': int(current_delivery)
            }

            if request.user.is_authenticated:
                context['disabled'] = 'disabled'

            return render(request, self.template_name, context=context)

        delivery_type = get_object_or_404(DeliveryType, id=int(current_delivery))

        def get_num():
            try:
                last_order = Order.objects.latest('number')
                return last_order.number + 1
            except Order.DoesNotExist:
                return  1001

        order = Order.objects.create(
            first_name=first_name, last_name=last_name, email=email, phone=phone, number=get_num(),
            delivery_type=delivery_type, zip_code=address['zip_code'], city=address['city'], address=address['address'], customer=user
        )

        if request.user.is_authenticated:
            LastUserAddress.objects.update_or_create(customer=request.user, address=address['address'], zip_code=address['zip_code'], city=address['city'])

        cart = Cart(request)
        cart_items = cart.get_items()

        print(cart_items)

        for i in cart_items:
            OrderItem.objects.create(
                order=order, product=i['product'], quantity=i['quantity'], 
                price=i['get_total_price'], size=i['size']
            )

        cart.clear()

        return redirect('orders')

    def test_func(self):
        if cart(self.request)['total_quantity'] == 0:
            raise Http404
        return True
