from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products, name='products'),
    path('search/', views.search, name='search'),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
