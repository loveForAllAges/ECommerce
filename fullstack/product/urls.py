from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductView.as_view(), name='main'),
    path('create-product/', views.CreateProductView.as_view(), name='create-product'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create-category'),
    path('create-size/', views.CreateSizeView.as_view(), name='create-size'),
    path('create-brand/', views.CreateBrandView.as_view(), name='create-brand'),
]
