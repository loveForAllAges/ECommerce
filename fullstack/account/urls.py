from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    # path('settings/', views.AccountEditView.as_view(), name='account-settings'),

    # # path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    
    # path("password-change/", views.CustomPasswordChangeView.as_view(), name='password-change'),

    # path("password-reset/", views.CustomPasswordResetView.as_view(),name="password_reset"),
    # path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # # path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('account', AccountAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('signup', SignupAPIView.as_view()),
    path('init', InitAPIView.as_view()),
]
