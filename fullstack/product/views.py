from typing import Any
from django.db import models
from .models import Product, ProductImage
from django.views.generic import DetailView
from config.utils import get_product_queryset
from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model


class ProductDetailView(DetailView):
    model = Product
    template_name = 'usage/product.html'

    def get_queryset(self):
        queryset = get_product_queryset(self.request)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            in_wishlist = Exists(get_user_model().objects.filter(
                id=self.request.user.id,
                wishlist=OuterRef('pk')
            ))
        else:
            in_wishlist = Exists()
        context['rec_list'] = Product.objects.prefetch_related('images').annotate(
            in_wishlist=in_wishlist
        )[:4]
        return context
