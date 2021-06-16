from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from base.models import Product, Order, OrderItem, ShippingAddress
# Create your views here.
from base.serializers import OrderSerializer


class AddOrderItem(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
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
                ShippingAddress=data['ShippingAddress'],
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
