from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Order
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from cart.context_processors import cart
from cart.cart import Cart
from address.models import Address


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'usage/orderList.html'

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user)


class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'orderDetail.html'

    def test_func(self, pk):
        user = self.request.user
        if not Order.objects.get(pk=pk, customer=user):
            raise Http404
        return True


class AdmOrderListView(UserPassesTestMixin, ListView):
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
        addresses = []
        if request.user.is_authenticated:
            addresses = Address.objects.filter(customer=request.user, is_deleted=False)
        context = {
            'order_form': OrderForm,
            'addresses': addresses
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
            user = request.user
        else:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            user = None

        Order.objects.create(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone, address=address, customer=user
        )

        cart = Cart(request)
        cart.clear()

        return HttpResponse('OK')

    def test_func(self):
        if cart(self.request)['total_quantity'] == 0:
            raise Http404
        return True
