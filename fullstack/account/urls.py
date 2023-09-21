from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path("change-password/", views.CustomPasswordChangeView.as_view(), name='change-password'),
    path('activate/<uidb64>/<token>/', views.ActivationView.as_view(), name='activate'),
    path('adm/users/', views.UserListView.as_view(), name='user-list'),


    # path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path("reset-password/", views.CustomPasswordResetView.as_view(),name="reset-password"),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    # path('adm/users/create/', views.UserCreateView.as_view(), name='user-create'),
    # path('adm/users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    # path('adm/users/delele/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),
]
