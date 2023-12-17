from django.urls import path
from . import views


urlpatterns = [
    path('products', views.ProductAPIView.as_view(), name='product_list_api'),
    path('products/<int:pk>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    # path('main-categories', views.MainCategoriesAPIView.as_view(), name='main_categories_list'),
    path('product-filters', views.ProductFiltersAPIView.as_view(), name='filter_list'),
    path('search', views.SearchAPIListView.as_view(), name='search_api'),
    path('home', views.HomeAPIView.as_view(), name='home_page_api'),
]
