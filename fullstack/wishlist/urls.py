from django.urls import path
from . import views


urlpatterns = [
    path('', views.WishlistView.as_view(), name='wishlist'),
]
