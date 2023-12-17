from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import *


api_urlpatterns = [
    path('cart/', include('cart.urls')),
    path('products/', include('product.urls')),
    path('orders/', include('order.urls')),
]


urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),

    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('catalog', TemplateView.as_view(template_name='pages/catalog.html'), name='catalog'),
    path('catalog/<int:pk>', TemplateView.as_view(template_name='pages/product_detail.html'), name='product_detail'),
    path('account', AccountTemplateView.as_view(), name='account_detail'),
    path('wishlist', WishlistTemplateView.as_view(), name='wish_list'),
    path('checkout', WishlistTemplateView.as_view(), name='checkout'),
    path('orders/<uuid:pk>', TemplateView.as_view(template_name='pages/order_detail.html'), name='order_detail'),

    path('api/', include(api_urlpatterns)),
    path('auth/', include('account.urls')),
    path('adm/', include('adm.urls')),


    path('fill_db', fill_db, name='fill_db'),
    path('fill_products', fill_products, name='fill_products'),
    path('fill_categories', fill_categories, name='fill_categories'),
    path('fill_deliveries', fill_deliveries, name='fill_deliveries'),
    path('fill_brands', fill_brands, name='fill_brands'),
    path('fill_sizes', fill_sizes, name='fill_sizes'),
    path('fill_search_history', fill_search_history, name='fill_search_history'),
]
 

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [
    # ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)