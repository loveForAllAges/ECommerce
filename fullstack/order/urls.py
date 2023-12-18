from django.urls import path, include

from .views import *


urlpatterns = [
    # path('', views.OrderListView.as_view(), name='order-list'),
    # path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),



    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),


    path('delivery/', DeliveryListAPIView.as_view()),

    path('orders/', OrderAPIView.as_view()),

]
