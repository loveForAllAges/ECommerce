from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/', views.ActivationView.as_view(), name='activate'),

    path('account/', views.AccountView.as_view(), name='account'),
    path('settings/', views.UserUpdateView.as_view(), name='settings'),

    path("password-change/", views.CustomPasswordChangeView.as_view(), name='password-change'),

    path("password-reset/", views.CustomPasswordResetView.as_view(),name="password_reset"),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('adm/users/', views.UserListView.as_view(), name='user-list'),
]
