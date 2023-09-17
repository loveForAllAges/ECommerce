from django.shortcuts import render
from .models import Product, Category, Size, Brand, ProductPhoto
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .forms import ProductForm, CategoryForm, SizeForm, BrandForm, ProductPhotoForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


class ProductListView(ListView):
    template_name = 'products.html'
    model = Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'usage/productDetail.html'


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
        photos = request.FILES.getlist('photos')
        if form.is_valid() and photos:
            product = form.save(commit=False)
            product.save()
            for photo in photos:
                ProductPhoto.objects.create(product=product, photo=photo)
            return redirect('main')
        return render(request, self.template_name, {'form': form})


class UpdateProductView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adm/createProduct.html'


# @method_decorator(staff_member_required, name='dispatch')
class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy('main')
    template_name = ''


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
