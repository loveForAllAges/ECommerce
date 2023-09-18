from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('adm/products/', views.AdmProductListView.as_view(), name='product-list'),
    path('adm/products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('adm/products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('adm/products/delele/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('adm/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('adm/categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('adm/categories/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('adm/categories/delele/<int:id>/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('adm/brands/', views.BrandListView.as_view(), name='brand-list'),
    path('adm/brands/create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('adm/brands/update/<int:pk>/', views.BrandUpdateView.as_view(), name='brand-update'),
    path('adm/brands/delete/<int:id>/', views.BrandDeleteView.as_view(), name='brand-delete'),
]
