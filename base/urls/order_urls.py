from django.urls import path

from base.views.order_views import AddOrderItem

urlpatterns = [
    path('add/', AddOrderItem.as_view(), name='orders-add'),
]
