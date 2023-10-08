from django.shortcuts import render
from django.views import View
from product.models import Brand, Category, Product
from django.db.models import Q


class StoreView(View):
    template_name = 'usage/store.html'

    def get(self, request):
        context = {}
        search_data = request.GET.get('search', '')

        context['object_list'] = Product.objects.filter(
            Q(name__icontains=search_data) | Q(description__icontains=search_data) | Q(brand__name__icontains=search_data) | Q(category__name__icontains=search_data)
        )
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['search_data'] = search_data

        return render(request, self.template_name, context)
