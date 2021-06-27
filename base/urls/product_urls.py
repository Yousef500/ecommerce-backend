from django.urls import path

from base.views.product_views import ProductListAPIView, ProductDetailAPIView, ProductDeleteAPIView, \
    ProductUpdateAPIView, uploadImage

urlpatterns = [
    path('', ProductListAPIView.as_view(), name="product-list"),
    path('upload/', uploadImage, name="image-upload"),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name="product-detail"),
    path('delete/<int:pk>/', ProductDeleteAPIView.as_view(), name="product-delete"),
    path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name="product-update"),
]
