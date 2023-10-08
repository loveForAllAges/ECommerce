from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    # path('<slug:slug>/', views.ProductCategoryListView.as_view(), name='category-detail'),
]
