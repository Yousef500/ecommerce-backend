from datetime import datetime

from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from base.models import Product, Order, OrderItem, ShippingAddress
# Create your views here.
from base.serializers import OrderSerializer


class AddOrderItem(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            serializer = OrderSerializer(Order.objects.all(), many=True)
            return Response(serializer.data)
        else:
            raise ValidationError({'detail': 'You are not authorized view all orders'})

    def post(self, request):
        user = self.request.user
        data = self.request.data
        orderItems = data['orderItems']

        if orderItems and len(orderItems) == 0:
            raise ValidationError({'detail': 'No Order Items'}, code=status.HTTP_400_BAD_REQUEST)
        else:
            # create order
            order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

            # create shipping address
            shipping = ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country']
            )

            # create the items and set order to orderItem relationship
            for o in orderItems:
                product = Product.objects.get(_id=o['product'])

                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    qty=o['qty'],
                    price=o['price'],
                    image=product.image.url
                )

                # update stock
                product.countInStock -= item.qty
                product.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data)


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            order = Order.objects.filter(_id=self.kwargs['pk'])
            if user.is_staff or order.values('user')[0]['user'] == user.id:
                return order
            else:
                raise ValidationError({'detail': 'Not Authorized to view this order'}, code=status.HTTP_400_BAD_REQUEST)
        except:
            raise ValidationError({'detail': 'Order does not exist'}, code=status.HTTP_400_BAD_REQUEST)


class OrderPayAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(isPaid=True, paidAt=datetime.now())
