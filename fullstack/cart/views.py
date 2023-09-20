from django.shortcuts import render
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from product.models import Product
from django.shortcuts import get_object_or_404
import json
from django.http import Http404
from django.contrib import messages


def cart_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('productId')
        action = data.get('action')
        
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if action in ['plus', 'minus']:
            cart.update(product, action)
        elif action == 'add':
            cart.add(product)
        elif action == 'delete':
            cart.delete(product)

        return HttpResponse('Updated')
    
    raise Http404
    

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.add_message(request, messages.SUCCESS, 'Корзина очищена')
    return render(request, 'usage/cartList.html')

#     if request.method == 'POST':
#         product_id = int(request.body.get('productId'))
#         action = request.body.get('action')
#         return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})


# def cart_delete(request):
#     if request.method == 'POST':
#         cart = Cart(request)
#         product_id = int(request.body.get('productId'))
#         product = get_object_or_404(Product, id=product_id)
#         cart.delete(product)
#         return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})


# def cart_add(request):
#     if request.method == 'POST':
#         cart = Cart(request)
#         product_id = int(request.body.get('productId'))
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product)
#         return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})
