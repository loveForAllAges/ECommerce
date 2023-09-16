from django.shortcuts import render
from .models import Product, Category, Size, Brand, ProductPhoto
from django.views import View
from django.views.generic import ListView, CreateView
from .forms import ProductForm, CategoryForm, SizeForm, BrandForm, ProductPhotoForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


class ProductView(ListView):
    template_name = 'products.html'
    model = Product


# class CreateProductView(CreateView):
#     template_name = 'createProduct.html'
#     form_class = ProductForm
#     success_url = reverse_lazy('main')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['items'] = Product.objects.all()
#         return context


class CreateProductView(View):
    template_name = 'createProduct.html'
    form_class = ProductForm

    def get(self, request):
        form1 = self.form_class()
        form2 = ProductPhotoForm()
        items = Product.objects.all()
        return render(request, self.template_name, {'form1': form1, 'form2': form2, 'items': items})

    def post(self, request):
        print(request.FILES)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            for photo in request.FILES.getlist('photos'):
                ProductPhoto.objects.create(product=product, photo=photo)
            return redirect('main')
        return render(request, self.template_name, {'form1': form1, 'form2': form2})


class CreateCategoryView(CreateView):
    template_name = 'createCategory.html'
    form_class = CategoryForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Category.objects.all()
        return context


class CreateSizeView(CreateView):
    template_name = 'createSize.html'
    form_class = SizeForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Size.objects.all()
        return context


class CreateBrandView(CreateView):
    template_name = 'createBrand.html'
    form_class = BrandForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Brand.objects.all()
        return context
