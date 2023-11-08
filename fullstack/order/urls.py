from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('delivery/', views.DeliveryListAPIView.as_view(), name='delivery-list'),
]
