from django.urls import path
from . import views


urlpatterns = [
    # path('', views.CartListView.as_view(), name='cart'),
    path('update/', views.cart_update, name='cart-update'),
    path('clear/', views.cart_clear, name='cart-clear'),
    # path('delete/', views.cart_delete, name='cart-delete'),
    path('<int:id>/add/', views.AddToCartView.as_view(), name='add-to-cart'),
]
