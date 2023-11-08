from django.shortcuts import render
from product.models import Product, ProductImage
from django.http import Http404
from product.forms import ProductForm
from django.views import View, generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from utils.imageManager import isImage, squareTheImage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from category.models import Category, Brand
from category.forms import CategoryForm, BrandForm


class AdmProductListView(UserPassesTestMixin, generic.ListView):
    model = Product
    template_name = 'adm/productList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True

class ProductCreateView(UserPassesTestMixin, View):
    template_name = 'adm/productCreate.html'
    form_class = ProductForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        photos = request.FILES.getlist('photos')
        error = False
        for photo in photos:
            if not isImage(photo):
                error = True
                messages.add_message(request, messages.ERROR, 'Файл не является изображением')
                break

        if form.is_valid() and photos and not error:
            product = form.save(commit=False)
            product.save()
            for photo in photos:
                new_filename, new_image = squareTheImage(photo)
                print(new_filename, new_image)
                new_photo = ProductImage.objects.create(product=product)
                new_photo.image.save(new_filename, new_image, save=False)

                new_photo.save()
                
            return redirect('product-list')
        return render(request, self.template_name, {'form': form})

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class ProductUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adm/productCreate.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class ProductDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('product-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
  

class CategoryListView(UserPassesTestMixin, generic.ListView):
    model = Category
    template_name = 'adm/categoryList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryCreateView(UserPassesTestMixin, generic.CreateView):
    template_name = 'adm/categoryCreate.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'adm/categoryCreate.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class BrandListView(UserPassesTestMixin, generic.ListView):
    model = Brand
    template_name = 'adm/brandList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandCreateView(UserPassesTestMixin, generic.CreateView):
    template_name = 'adm/brandCreate.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Brand
    fields = '__all__'
    template_name = 'adm/brandCreate.html'
    success_url = reverse_lazy('brand-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Brand
    success_url = reverse_lazy('brand-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
