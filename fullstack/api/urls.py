from django.urls import path
from . import views


urlpatterns = [
    # path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),

    path('search/', views.search, name='search'),
    
    path('wishlist/', views.WishlistAPIView.as_view()),

    path('delivery/', views.DeliveryListAPIView.as_view(), name='delivery-list'),

    path('orders/', views.OrderAPIView.as_view(), name='order-create'),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
