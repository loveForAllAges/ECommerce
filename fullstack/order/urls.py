from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('cart/update/', views.cart_update, name='cart-update'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),

    # path('adm/orders/', views.OrderListView.as_view(), name='adm-order-list'),
    # path('adm/orders/create/', views.OrderListView.as_view(), name='order-create'),
    # path('adm/orders/<int:pk>/', views.OrderListView.as_view(), name='order-detail'),
    # path('adm/orders/update/<int:pk>/', views.OrderListView.as_view(), name='order-update'),
    # path('adm/orders/delete/<int:pk>/', views.OrderListView.as_view(), name='order-delete'),
]
