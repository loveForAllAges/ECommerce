from typing import Any
from django.shortcuts import render
from .models import Product, Category, Brand, ProductPhoto
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .forms import ProductForm, CategoryForm, BrandForm, ProductPhotoForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


class ProductListView(ListView):
    template_name = 'usage/productList.html'
    model = Product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['cookie'] = self.request.COOKIES
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'usage/productDetail.html'


class AdmProductListView(ListView):
    model = Product
    template_name = 'adm/productList.html'


class ProductCreateView(View):
    template_name = 'adm/productCreate.html'
    form_class = ProductForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        photos = request.FILES.getlist('photos')
        if form.is_valid() and photos:
            product = form.save(commit=False)
            product.save()
            for photo in photos:
                ProductPhoto.objects.create(product=product, photo=photo)
            return redirect('product-list')
        return render(request, self.template_name, {'form': form})


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adm/productCreate.html'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product-list')
    template_name = ''


# -----


class CategoryListView(ListView):
    model = Category
    template_name = 'adm/categoryList.html'


class CategoryCreateView(CreateView):
    template_name = 'adm/categoryCreate.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'adm/categoryCreate.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = ''


# -----


class BrandListView(ListView):
    model = Brand
    template_name = 'adm/brandList.html'


class BrandCreateView(CreateView):
    template_name = 'adm/brandCreate.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand-list')


class BrandUpdateView(UpdateView):
    model = Brand
    fields = '__all__'
    template_name = 'adm/brandCreate.html'
    success_url = reverse_lazy('brand-list')


class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('brand-list')
    template_name = ''
