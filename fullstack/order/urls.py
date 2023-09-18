from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('cart/update/<int:pk>/<str:act>/', views.CartListView.as_view(), name='cart-update'),
    path('cart/create/<int:pk>/', views.CartListView.as_view(), name='cart-create'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),

    # path('adm/orders/', views.OrderListView.as_view(), name='adm-order-list'),
    # path('adm/orders/create/', views.OrderListView.as_view(), name='order-create'),
    # path('adm/orders/<int:pk>/', views.OrderListView.as_view(), name='order-detail'),
    # path('adm/orders/update/<int:pk>/', views.OrderListView.as_view(), name='order-update'),
    # path('adm/orders/delete/<int:pk>/', views.OrderListView.as_view(), name='order-delete'),
]
