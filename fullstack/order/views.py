from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Order, OrderItem, Delivery, ORDER_CHOICES
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from cart.cart import Cart
from account.models import Address
from order.forms import OrderForm


# class OrderListView(LoginRequiredMixin, ListView):
#     template_name = 'usage/orders.html'

#     def get_queryset(self):
#         queryset = Order.objects.filter(customer=self.request.user).order_by('-number')
#         return queryset


class OrderDetailView(DetailView):
    model = Order
    template_name = 'usage/orderDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exc = 3 if context['object'].delivery.slug == 'pickup' else None
        context['statuses'] = tuple(filter(lambda choice: choice[0] != exc, ORDER_CHOICES))
        return context


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
