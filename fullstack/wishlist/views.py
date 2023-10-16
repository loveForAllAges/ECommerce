from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from product.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class WishlistView(View):
    template_name = 'usage/wishlist.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        if not self.request.user.is_anonymous:
            data = json.loads(request.body)
            product_id = data.get('productId')
            print(product_id)
            if not request.user.wishlist.filter(id=product_id).exists():
                product = get_object_or_404(Product, id=product_id)
                request.user.wishlist.add(product)
                messages.add_message(self.request, messages.SUCCESS, 'Товар добавлен в избранное')
        else:
            messages.add_message(self.request, messages.ERROR, 'Авторизируйтесь, чтобы добавлять товары в избранное')

        return HttpResponse()


    def delete(self, request):
        data = json.loads(request.body)
        product_id = data.get('productId')
        if request.user.wishlist.filter(id=product_id).exists():
            product = get_object_or_404(Product, id=product_id)
            request.user.wishlist.remove(product)
            messages.add_message(self.request, messages.SUCCESS, 'Товар убран из избранного')

        return HttpResponse(200)
