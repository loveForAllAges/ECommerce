from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.AddressCreateView.as_view(), name='address-create'),
    path('make-main/', views.address_make_main, name='address-make-main'),
    path('edit/<int:pk>/', views.AddressUpdateView.as_view(), name='address-update'),
    path('delete/', views.address_delete, name='address-delete'),
]