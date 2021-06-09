from django.urls import path

from .views import getRoutes, ProductListAPIView, ProductDetailAPIView, MyTokenObtainPairView

urlpatterns = [
    path('users/login/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('', getRoutes, name="routes"),
    path('products/', ProductListAPIView.as_view(), name="products-list"),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name="products-detail"),
]
