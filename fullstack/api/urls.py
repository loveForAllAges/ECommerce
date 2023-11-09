from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('search/', views.search, name='search'),
    path('wishlist/', views.WishlistAPIView.as_view()),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
