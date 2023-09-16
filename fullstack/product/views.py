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
        form = self.form_class()
        image_formset = ProductPhotoForm()
        items = Product.objects.all()
        return render(request, self.template_name, {'form': form, 'image_formset': image_formset, 'items': items})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid() and request.FILES.getlist('photos'):
            product = form.save(commit=False)
            product.save()
            for image in request.FILES.getlist('images'):
                ProductPhoto.objects.create(product=product, image=image)
            return redirect('main')
        return render(request, self.template_name, {'form': form})


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
