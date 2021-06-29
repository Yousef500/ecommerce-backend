from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from base.models import Product, Review
# Create your views here.
from base.serializers import ProductSerializer


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save(user=user)
        else:
            raise ValidationError({'detail': 'You are not authorized to create products'},
                                  code=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    # def perform_update(self, serializer):
    #     product = Product.objects.get(name=self.request.data['name'])
    #     if self.request.data['image']:
    #         serializer.save(image=self.request.data['image'])
    #     else:
    #         serializer.save(image=product.image)


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product = Product.objects.get(_id=data['product_id'])

    product.image = request.FILES.get("image")
    product.save()

    return Response('Image was uploaded');
