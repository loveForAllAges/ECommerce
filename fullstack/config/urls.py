from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def create_test_db(request):
    return render(request, 'errors/404.html')
    # from product.models import Brand, Product, Category

    # for i in range(1, 10):
    #     brand = Brand.objects.create(name=f'Brand {i}')
    #     category = Category.objects.create(name=f'Category {i}')

    #     Product.objects.create(
    #         name=f'Product {i}',
    #         description=f'Description {i}',
    #         price=i*10,
    #         brand=brand,
    #         category=category
    #     )


urlpatterns = [
    # path('404/', create_test_db),
    path('address/', include('address.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('', include('order.urls')),
    path('', include('account.urls')),
    path('', include('product.urls')),
]

# print(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)