from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('address/create/', views.AddressCreateView.as_view(), name='address-create'),
    path('address/edit/<int:pk>/', views.AddressUpdateView.as_view(), name='address-update'),
    path('address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='address-delete'),
    path('cart/update/', views.cart_update, name='cart-update'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('adm/orders/', views.OrderListView.as_view(), name='order-list'),
    # path('adm/orders/create/', views.OrderListView.as_view(), name='order-create'),
    # path('adm/orders/<int:pk>/', views.OrderListView.as_view(), name='order-detail'),
    # path('adm/orders/update/<int:pk>/', views.OrderListView.as_view(), name='order-update'),
    # path('adm/orders/delete/<int:pk>/', views.OrderListView.as_view(), name='order-delete'),
]
