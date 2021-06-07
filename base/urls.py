from django.urls import path

from .views import getRoutes, ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('', getRoutes, name="routes"),
    path('products/', ProductListAPIView.as_view(), name="products-list"),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name="products-detail"),
]
