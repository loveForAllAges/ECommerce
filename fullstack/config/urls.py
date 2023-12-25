from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


api_urlpatterns = [
    path('cart/', include('cart.urls')),
    path('products/', include('product.urls')),
    path('orders/', include('order.urls')),
]


urlpatterns = [
    path('', include('frontend.urls')),
    path("__debug__/", include('debug_toolbar.urls')),
    path('account/', include('account.urls')),
    path('api/', include(api_urlpatterns)),
]
 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
