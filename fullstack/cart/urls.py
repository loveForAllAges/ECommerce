from django.urls import path
from . import views


urlpatterns = [
    path('update/', views.cart_update, name='cart-update'),
    path('delete/', views.cart_delete, name='cart-delete'),
    path('create/', views.cart_create, name='cart-create'),
]
