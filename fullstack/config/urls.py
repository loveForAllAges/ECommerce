from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def get_cookies(request):
    sk = request.COOKIES.get('cart')
    return HttpResponse([sk])


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('', include('account.urls')),
    path('', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('cookies', get_cookies),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)