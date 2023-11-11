from django.urls import path
from . import views


urlpatterns = [
    # path('', views.OrderListView.as_view(), name='order-list'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
