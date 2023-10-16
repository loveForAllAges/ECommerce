from django.urls import path
from . import views


urlpatterns = [
    path('', views.AddressView.as_view(), name='address'),
    path('<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address-delete'),
]
