from django.urls import path

from base.views.order_views import AddOrderItem, OrderDetailAPIView

urlpatterns = [
    path('add/', AddOrderItem.as_view(), name='orders-add'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
