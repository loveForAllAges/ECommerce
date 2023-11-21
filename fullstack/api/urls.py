from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'products', views.ProductViewset)



urlpatterns = [
    path('products', views.ProductAPIView.as_view()),
    # path('', include(router.urls)),
    # path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),


    path('main-categories', views.MainCategoriesAPIView.as_view()),
    path('product-filters', views.ProductFiltersAPIView.as_view()),

    # path('search/', views.search, name='search'),
    
    path('wishlist/', views.WishlistAPIView.as_view()),

    path('delivery/', views.DeliveryListAPIView.as_view(), name='delivery-list'),

    path('orders/', views.OrderAPIView.as_view(), name='order-create'),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
