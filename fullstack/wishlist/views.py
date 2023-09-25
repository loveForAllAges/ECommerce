from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
# from .models import Wishlist
from product.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class WishlistView(LoginRequiredMixin, View):
    template_name = 'usage/wishlistList.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('productId')
        print(product_id)
        if not request.user.wishlist.filter(id=product_id).exists():
            product = get_object_or_404(Product, id=product_id)
            request.user.wishlist.add(product)
            print('OK')

        return HttpResponse(200)


    def delete(self, request):
        data = json.loads(request.body)
        product_id = data.get('productId')
        if request.user.wishlist.filter(id=product_id).exists():
            product = get_object_or_404(Product, id=product_id)
            request.user.wishlist.remove(product)

        return HttpResponse(200)
