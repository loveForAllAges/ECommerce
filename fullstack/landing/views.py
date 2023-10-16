from django.shortcuts import render
from product.models import Product, Brand
from django.views import View
from django.db.models import Q


class MainView(View):
    template_name = 'landing.html'

    def get(self, request):
        context = {}
        search_data = request.GET.get('search', '')

        context['product_list'] = Product.objects.all()
        context['new_product_list'] = Product.objects.order_by('-id')[:8]
        context['brands'] = Brand.objects.all()
        context['search_data'] = search_data

        return render(request, self.template_name, context)
    