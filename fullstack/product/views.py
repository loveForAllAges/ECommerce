from .models import Product, ProductImage
from django.views.generic import DetailView
 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'usage/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rec_list'] = Product.objects.all()[:4]
        context['images'] = ProductImage.objects.filter(product=kwargs['object'])
        return context
