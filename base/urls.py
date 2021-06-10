from django.urls import path

from .views import ProductListAPIView, ProductDetailAPIView, MyTokenObtainPairView, UserProfileAPIView, \
    UserListAPIView, UserCreateAPIView

urlpatterns = [
    path('users/login/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('users/profile/', UserProfileAPIView.as_view(), name="user-profile"),
    path('users/register/', UserCreateAPIView.as_view(), name="user-create"),
    path('users/', UserListAPIView.as_view(), name="user-list"),
    path('products/', ProductListAPIView.as_view(), name="product-list"),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name="product-detail"),
]
