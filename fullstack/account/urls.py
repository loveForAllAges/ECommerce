from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('edit/', views.AccountEditView.as_view(), name='account-edit'),
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/', views.ActivationView.as_view(), name='activate'),

    path("password-change/", views.CustomPasswordChangeView.as_view(), name='password-change'),

    path("password-reset/", views.CustomPasswordResetView.as_view(),name="password_reset"),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('adm/users/', views.UserListView.as_view(), name='user-list'),
]
