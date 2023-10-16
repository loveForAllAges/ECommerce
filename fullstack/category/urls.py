from django.urls import path
from . import views


urlpatterns = [
    path('', views.CategoryView.as_view(), name='category'),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
