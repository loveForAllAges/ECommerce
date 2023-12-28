from django.urls import path, include

from .views import *


urlpatterns = [
    # path('', views.OrderListView.as_view(), name='order-list'),
    # path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),


    path('checkout/', CheckoutAPIView.as_view()),
]
