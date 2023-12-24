from django.urls import path, include

from . import views


urlpatterns = [
    path('<int:pk>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('catalog/', views.CatalogListAPIView.as_view(), name='product_catalog_api'),
    path('more', views.MoreProductAPIView.as_view(), name='more_products_api'),
    path('wish', views.WishAPIView.as_view(), name='product_wish_api'),
    path('search', views.SearchListAPIView.as_view(), name='product_search_api'),
    path('home', views.HomeAPIView.as_view(), name='product_home_api'),
]
