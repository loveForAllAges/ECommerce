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
from account.models import Address
from django.shortcuts import get_object_or_404

from rest_framework import views, generics, response, status, permissions
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


class DeliveryListAPIView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class CartExists(permissions.BasePermission):
    def has_permission(self, request, view):
        cart = Cart(request)
        if len(cart):
            return True
        return False


class OrderAPIView(views.APIView):
    permission_classes = [CartExists]

    def post(self, request):
        data = request.data.copy()
        if data['delivery'] != 'pickup' and not (data['address'] and data['zip_code'] and data['city']):
            return response.Response({'message': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)
        
        if data['delivery'] == 'pickup':
            data['city'] = ''
            data['address'] = ''
            data['zip_code'] = ''

        if self.request.user.is_authenticated:
            data['first_name'] = self.request.user.first_name
            data['last_name'] = self.request.user.last_name
            data['email'] = self.request.user.email
            data['phone'] = self.request.user.phone
            data['customer'] = self.request.user.pk

            if data['delivery'] != 'pickup':
                address, created = Address.objects.get_or_create(customer=request.user)
                address.city = data['city']
                address.address = data['address']
                address.zip_code = data['zip_code']
                address.save()
        data['delivery'] = str(Delivery.objects.get(slug=data['delivery']).pk)
        
        order_serializer = OrderSerializer(data=data, context={'request': self.request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        cart = Cart(request)

        for i in cart.get_cart()['goods']:
            OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price'], size_id=i['size']['id']
            )

        return response.Response({'data': order_serializer.data, 'success': True}, status=status.HTTP_200_OK)


class CheckoutView(UserPassesTestMixin, View):
    template_name = 'usage/checkout.html'

    def get(self, request):
        context = {
            'form': OrderForm,
        }
        if request.user.is_authenticated:
            address = Address.objects.filter(customer=request.user)
            if address:
                context['address'] = address[0]
            context['first_name'] = request.user.first_name
            context['last_name'] = request.user.last_name
            context['email'] = request.user.email
            context['phone'] = request.user.phone
            context['disabled'] = 'disabled'

        return render(request, self.template_name, context=context)

    def test_func(self):
        cart = Cart(self.request)
        if not len(cart):
            raise Http404
        return True
