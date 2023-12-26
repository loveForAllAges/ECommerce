from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import *


urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('catalog', TemplateView.as_view(template_name='pages/catalog.html'), name='catalog'),
    path('catalog/<int:pk>', TemplateView.as_view(template_name='pages/product_detail.html'), name='product_detail'),
    path('wishlist/', WishlistTemplateView.as_view(), name='wish_list'),
    path('checkout', WishlistTemplateView.as_view(), name='checkout'),
    path('orders/<uuid:pk>', TemplateView.as_view(template_name='pages/order_detail.html'), name='order_detail'),
    
    path('account/', AccountTemplateView.as_view(), name='account_detail'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('signup/', SignupTemplateView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateTemplateView.as_view(), name='activate'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),

    path("password-reset/", TemplateView.as_view(template_name='pages/signup.html'), name="password_reset"),
    path('password-reset-done/', TemplateView.as_view(template_name='pages/signup.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', TemplateView.as_view(template_name='pages/signup.html'), name='password_reset_confirm'),

    path('adm/', include('adm.urls')),

    path('fill_db', fill_db, name='fill_db'),
]
