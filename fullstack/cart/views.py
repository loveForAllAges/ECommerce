from django.shortcuts import render, redirect
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from product.models import Product
from django.shortcuts import get_object_or_404
import json
from django.http import Http404
from django.contrib import messages
from django.views import View
from django.contrib import messages
from category.models import Size


class AddToCartView(View):
    def post(self, request, id):
        size = request.POST.get('size')

        size = get_object_or_404(Size, id=int(size))
        product = get_object_or_404(Product, id=id)

        cart = Cart(request)
        cart.add(product, size)

        messages.add_message(request, messages.SUCCESS, 'Товар добавлен в корзину')
        return redirect('product', id)


# class CartListView(ListView):
#     template_name = 'usage/cart.html'

#     def get_queryset(self):
#         queryset = ''
#         return queryset


def cart_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('productId')
        action = data.get('action')
        size_id = data.get('sizeId')
        
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id)

        if action in ['plus', 'minus']:
            cart.update(product, action, size)
            messages.add_message(request, messages.SUCCESS, 'Товар добавлен в корзину')
        elif action == 'add':
            cart.add(product, size)
            messages.add_message(request, messages.SUCCESS, 'Товар добавлен в корзину')
        elif action == 'delete':
            cart.delete(product, size)
            messages.add_message(request, messages.SUCCESS, 'Товар удален из корзины')

        return HttpResponse('Updated')
    
    raise Http404
    

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.add_message(request, messages.SUCCESS, 'Корзина очищена')
    return render(request, 'usage/cartList.html')
