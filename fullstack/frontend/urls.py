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
    path('checkout', CheckoutTemplateView.as_view(), name='checkout'),
    path('orders/<uuid:pk>', OrderTemplateView.as_view(), name='order_detail'),
    
    path('account/', AccountTemplateView.as_view(), name='account_detail'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('signup/', SignupTemplateView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateTemplateView.as_view(), name='activate'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),

    path("password_reset/", PasswordResetTemplateView.as_view(), name="password_reset"),
    path('password_reset/<uidb64>/<token>/', PasswordResetProcessTemplateView.as_view(), name='password_reset_process'),

    path('adm/', include('adm.urls')),

    path('fill_db', fill_db, name='fill_db'),
]
