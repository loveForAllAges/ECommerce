from django.urls import path
from . import views


urlpatterns = [
    path('products', views.ProductAPIView.as_view(), name='product_list_api'),
    path('products/<int:pk>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('wish', views.ProductWishAPIView.as_view(), name='product_wish_api'),
    path('filters', views.ProductFiltersAPIView.as_view(), name='product_filters_api'),
    path('search', views.SearchAPIListView.as_view(), name='product_search_api'),
    path('home', views.HomeAPIView.as_view(), name='product_home_api'),
]
