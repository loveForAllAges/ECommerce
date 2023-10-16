from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    # path('adm/orders/', views.OrderListView.as_view(), name='order-list'),
    # path('adm/orders/create/', views.OrderListView.as_view(), name='order-create'),
    # path('adm/orders/<int:pk>/', views.OrderListView.as_view(), name='order-detail'),
    # path('adm/orders/update/<int:pk>/', views.OrderListView.as_view(), name='order-update'),
    # path('adm/orders/delete/<int:pk>/', views.OrderListView.as_view(), name='order-delete'),
]
