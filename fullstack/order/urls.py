from django.urls import path
from . import views


urlpatterns = [
    # path('', views.OrderListView.as_view(), name='order-list'),
    # path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),



    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('wishlist/', views.WishlistAPIView.as_view()),

    path('delivery/', views.DeliveryListAPIView.as_view()),

    path('orders/', views.OrderAPIView.as_view()),

]
