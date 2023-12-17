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


# class OrderDetailView(DetailView):
#     model = Order
#     template_name = 'usage/order.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         exc = 3 if context['object'].delivery.slug == 'pickup' else None
#         context['statuses'] = tuple(filter(lambda choice: choice[0] != exc, ORDER_CHOICES))
#         return context


# class CheckoutView(UserPassesTestMixin, View):
#     template_name = 'usage/checkout.html'

#     def get(self, request):
#         context = {
#             'form': OrderForm,
#         }
#         if request.user.is_authenticated:
#             address = Address.objects.filter(customer=request.user)
#             if address:
#                 context['address'] = address[0]
#             context['first_name'] = request.user.first_name
#             context['last_name'] = request.user.last_name
#             context['email'] = request.user.email
#             context['phone'] = request.user.phone
#             context['disabled'] = 'disabled'

#         return render(request, self.template_name, context=context)

#     def test_func(self):
#         cart = Cart(self.request)
#         if not len(cart):
#             raise Http404
#         return True


from order.serializers import DeliverySerializer, OrderSerializer

from cart.cart import Cart

from config.permissions import IsStaffOrReadOnly, IsAuthenticatedOrCreateOnly, CartExists
from config.utils import send_email
from product.utils import get_product_queryset
from product.models import Product, Brand, Size, SearchHistory
from product.serializers import ProductSerializer, MainCategorySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from account.models import Address
from rest_framework import views, status, response, generics
from django.db.models import OuterRef, Exists
from django.contrib.auth import get_user_model


User = get_user_model()


class WishlistAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            product_id = data.get('product_id')
            product = Product.objects.annotate(
                in_wishlist=~Exists(User.objects.filter(
                    id=self.request.user.id,
                    wishlist=OuterRef('pk')
                ))
            ).get(id=product_id)
            if request.user.wishlist.filter(id=product_id).exists():
                request.user.wishlist.remove(product)
            else:
                request.user.wishlist.add(product)
            serializer = ProductSerializer(product, context={'request': self.request})
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return response.Response({'message': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryListAPIView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrderAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly, CartExists]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
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
        data['delivery'] = Delivery.objects.get(slug=data['delivery']).pk
        
        order_serializer = OrderSerializer(data=data, context={'request': self.request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        cart = Cart(request)
        url = request.build_absolute_uri(order.url())

        for i in cart.get_cart()['goods']:
            item = OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price']
            )
            if i['size']:
                item.size_id = i['size']['id']
                item.save()

        cart.clear()

        send_email(request, request.user, 'Заказ оформлен', f'Заказ успешно оформлен! Отслеживание заказа: {url}')
        message = 'Заказ оформлен. На почту отправлено дублирующее письмо.'
        return response.Response({'url': url, 'message': message}, status=status.HTTP_200_OK)
