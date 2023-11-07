from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Order, OrderItem, Delivery, ORDER_CHOICES
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import OrderForm, PersonForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from cart.cart import Cart
from account.models import LastUserAddress
from django.shortcuts import get_object_or_404

from rest_framework import views, generics, response, status
from .serializers import DeliverySerializer, OrderSerializer, OrderItemSerializer
import json


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'usage/orders.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).order_by('-number')
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


class DeliveryListAPIView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


# class OrderAPIView(generics.CreateAPIView):
#     serializer_class = OrderSerializer

#     def perform_create(self, serializer):
#         print(self)
#         if self.request.is_authenticated:
#             serializer.save(customer=self.request.user, first_name=self.request.user.first_name, last_name=self.request.user.last_name)
#         else:
#             serializer.save()
        # return super().perform_create(serializer)


class OrderAPIView(views.APIView):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    def get(self, request):
        data = Order.objects.all()
        serializer = OrderSerializer(data, many=True, context={'request': self.request})
        return response.Response(serializer.data)
        # return response.Response(self.serializer_class(self.queryset).data)

    def post(self, request):
        data = request.data
        try:
            clear_data = {
                'address': data.get('address', None),
                'zip_code': data.get('zip_code', None),
                'city': data.get('address', None),
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'delivery': int(data.get('delivery', '')),
                # 'goods': cart.get_cart()['goods']
            }
            order_serializer = OrderSerializer(data=clear_data)
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save()

            if self.request.user.is_authenticated:
                order.first_name = self.request.user.first_name
                order.last_name = self.request.user.last_name
                order.email = self.request.user.email
                order.phone = self.request.user.phone
                order.customer = self.request.user
                order.save()

            cart = Cart(request)

            for i in cart.get_cart()['goods']:
                OrderItem.objects.create(
                    order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                    price=i['total_price'], size_id=i['size']['id']
                )
        except Exception as ex:
            print('err', ex)
            # return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # print(clear_data)
        # print(sr.is_valid(), sr.data)
        return response.Response({'error': 'error'}, status=status.HTTP_404_NOT_FOUND)


class CheckoutView(UserPassesTestMixin, View):
    template_name = 'usage/checkout.html'

    def get(self, request):
        context = {
            'form': OrderForm,
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
                'delivery_types': Delivery.objects.all(),
                'current_delivery': int(current_delivery)
            }

            if request.user.is_authenticated:
                context['disabled'] = 'disabled'

            return render(request, self.template_name, context=context)

        delivery_type = get_object_or_404(Delivery, id=int(current_delivery))

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
        cart_items = cart.get_cart()

        print(cart_items)

        for i in cart_items['goods']:
            print('\n\n', i)
            OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price'], size_id=i['size']['id']
            )

        # cart.clear()

        return redirect('order', order.pk)

    def test_func(self):
        cart = Cart(self.request)
        if not len(cart):
            raise Http404
        return True
