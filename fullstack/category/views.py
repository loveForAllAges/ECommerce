from django.views import View
from product.models import Product
from category.models import Category, Color, Size, Brand
from django.shortcuts import render
from django.db.models import Q, When, Case, Value, BooleanField


class AllCategoriesView(View):
    template_name = 'usage/store.html'

    def get(self, request):
        context = {}
        context['object_list'] = Product.objects.all()
        context['brand_list'] = Brand.objects.all()
        context['category_type_list'] = Category.objects.filter(parent__isnull=False)
        context['size_list'] = Size.objects.all()
        context['color_list'] = Color.objects.all()
        return render(request, self.template_name, context)


class CategoryView(View):
    template_name = 'usage/store.html'

    def get(self, request):
        context = {}
        category_list = request.GET.getlist('category', '')
        type_list = request.GET.getlist('type', '')
        color_list = request.GET.getlist('color', '')
        brand_list = request.GET.getlist('brand', '')
        size_list = request.GET.getlist('size', '')
        sort_type = request.GET.get('sort', '')
        query = request.GET.get('q', '')
        
        filters = Q()

        if category_list:
            filters &= Q(category__parent__slug__in=category_list)

        if type_list:
            filters &= Q(category__slug__in=type_list)

        if color_list:
            filters &= Q(color__slug__in=color_list)

        if brand_list:
            filters &= Q(brand__slug__in=brand_list)

        if size_list:
            filters &= Q(size__slug__in=size_list)

        if query:
            filters &= Q(name__icontains=query) | Q(brand__name__icontains=query) | Q(brand__slug__icontains=query)

        context['product_list'] = Product.objects.filter(filters).distinct()

        if sort_type:
            if sort_type == 'new':
                context['product_list'] = context['product_list'].order_by('-id')
            elif sort_type == 'cheaper':
                context['product_list'] = context['product_list'].order_by('price')
            elif sort_type == 'expensive':
                context['product_list'] = context['product_list'].order_by('-price')

        context['active_category_tags'] = category_list
        context['active_type_tags'] = type_list
        context['active_brand_tags'] = brand_list
        context['active_color_tags'] = color_list
        context['active_size_tags'] = size_list
        context['total_active_tags_count'] = len(size_list) + len(category_list) + len(type_list) + len(brand_list) + len(color_list)

        context['brand_list'] = Brand.objects.all()
        context['category_type_list'] = Category.objects.filter(parent__isnull=False)
        context['size_list'] = Size.objects.all()
        context['color_list'] = Color.objects.all()
        
        return render(request, self.template_name, context)
