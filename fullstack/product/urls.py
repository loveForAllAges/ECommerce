from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'catalog', views.CatalogViewSet, basename='product_catalog_api')


urlpatterns = [
    path('', include(router.urls)),

    path('more', views.MoreProductAPIView.as_view(), name='more_products_api'),
    # path('products/<int:pk>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('wish', views.WishAPIView.as_view(), name='product_wish_api'),
    path('search', views.SearchListAPIView.as_view(), name='product_search_api'),
    path('home', views.HomeAPIView.as_view(), name='product_home_api'),
]
