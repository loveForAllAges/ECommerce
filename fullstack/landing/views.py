from django.shortcuts import render
from product.models import Product, Brand
from django.views import View
from django.db.models import Q


class MainView(View):
    template_name = 'landing.html'

    def get(self, request):
        context = {}
        search_data = request.GET.get('search', '')

        context['shoes_list'] = Product.objects.filter(category__parent__slug='shoes').order_by('-id')[:4]
        context['accessories_list'] = Product.objects.filter(category__parent__slug='accessories').order_by('-id')[:4]
        context['clothes_list'] = Product.objects.filter(category__parent__slug='clothes').order_by('-id')[:4]
        context['new_product_list'] = Product.objects.order_by('-id')[:4]
        context['search_data'] = search_data

        return render(request, self.template_name, context)
    