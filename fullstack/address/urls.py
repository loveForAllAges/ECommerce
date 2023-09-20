from django.urls import path
from . import views


urlpatterns = [
    path('address/create/', views.AddressCreateView.as_view(), name='address-create'),
    path('address/edit/<int:pk>/', views.AddressUpdateView.as_view(), name='address-update'),
    path('address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='address-delete'),
]
