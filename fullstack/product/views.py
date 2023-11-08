from django.shortcuts import render
from .models import Product, Category, Brand, ProductImage
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'usage/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rec_list'] = Product.objects.all()[:4]
        context['images'] = ProductImage.objects.filter(product=kwargs['object']).order_by('-is_main')
        return context
