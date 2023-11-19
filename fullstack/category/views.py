from django.views import View
from product.models import Product
from category.models import Category, Size, Brand
from django.shortcuts import render
from django.db.models import Q, When, Case, Value, BooleanField


# class AllCategoriesView(View):
#     template_name = 'usage/store.html'

#     def get(self, request):
#         context = {}
#         context['object_list'] = Product.objects.all()
#         context['brand_list'] = Brand.objects.all()
#         context['category_type_list'] = Category.objects.filter(parent__isnull=False)
#         context['size_list'] = Size.objects.all()
#         return render(request, self.template_name, context)


class CategoryView(View):
    template_name = 'usage/store.html'

    def get(self, request):
        context = {}
        category_list = request.GET.get('category', '')
        color_list = request.GET.get('color', '')
        brand_list = request.GET.get('brand', '')
        size_list = request.GET.get('size', '')
        # sort_type = request.GET.get('sort', '')
        # search = request.GET.get('search', '')
        
        # filters = Q()

        # if category_list:
        #     filters &= Q(category__parent__slug__in=category_list)

        # if type_list:
        #     filters &= Q(category__slug__in=type_list)

        # if color_list:
        #     filters &= Q(color__slug__in=color_list)

        # if brand_list:
        #     filters &= Q(brand__slug__in=brand_list)

        # if size_list:
        #     filters &= Q(size__slug__in=size_list)

        # if search:
            # context['search'] = search
            # filters &= Q(name__icontains=search) | Q(brand__name__icontains=search) | Q(brand__slug__icontains=search)

        # context['product_list'] = Product.objects.filter(filters).distinct()

        # if sort_type:
        #     if sort_type == 'new':
        #         context['product_list'] = context['product_list'].order_by('-id')
        #     elif sort_type == 'cheaper':
        #         context['product_list'] = context['product_list'].order_by('price')
        #     elif sort_type == 'expensive':
        #         context['product_list'] = context['product_list'].order_by('-price')
        context['active_category_tags'] = map(int, category_list.split(','))
        context['active_brand_tags'] = map(int, brand_list.split(','))
        context['active_color_tags'] = map(int, color_list.split(','))
        context['active_size_tags'] = map(int, size_list.split(','))

        context['brand_list'] = Brand.objects.all()
        context['category_type_list'] = Category.objects.filter(parent__isnull=False)
        context['size_list'] = Size.objects.all()
        
        return render(request, self.template_name, context)
