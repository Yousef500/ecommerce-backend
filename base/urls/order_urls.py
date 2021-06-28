from django.urls import path

from base.views.order_views import ListAddOrderItem, OrderDetailAPIView, OrderPayAPIView, OrderDeliverAPIView

urlpatterns = [
    path('', ListAddOrderItem.as_view(), name='orders-list-create'),
    path('<int:pk>/deilver/', OrderDeliverAPIView.as_view(), name='order-deliver'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('<int:pk>/pay', OrderPayAPIView.as_view(), name='order-pay'),
]
