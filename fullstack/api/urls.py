from django.urls import path
from . import views


urlpatterns = [
    path('products', views.ProductAPIView.as_view()),
    path('products/<int:pk>', views.ProductDetailAPIView.as_view()),

    path('main-categories', views.MainCategoriesAPIView.as_view()),
    path('product-filters', views.ProductFiltersAPIView.as_view()),
    
    path('wishlist/', views.WishlistAPIView.as_view()),

    path('delivery/', views.DeliveryListAPIView.as_view()),

    path('orders/', views.OrderAPIView.as_view()),
]
