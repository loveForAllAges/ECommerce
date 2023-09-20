from django.shortcuts import render
from .cart import Cart
from django.http import HttpResponse, JsonResponse
from product.models import Product
from django.shortcuts import get_object_or_404


def cart_update(request):
    cart = Cart(request)
    product_id = 2
    product = get_object_or_404(Product, id=product_id)
    cart.update(product, 'plus')
    return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})


def cart_delete(request):
    cart = Cart(request)
    product_id = 1
    product = get_object_or_404(Product, id=product_id)
    cart.delete(product)
    return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})


def cart_add(request):
    if request.method == 'POST':
        pass
    cart = Cart(request)

    # product_id = int(request.POST.get('product_id'))
    product_id = 2
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)

    return JsonResponse({'total_price': cart.get_total_price(), 'total_quantity': len(cart)})
