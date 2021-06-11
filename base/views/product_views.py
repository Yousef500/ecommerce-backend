from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.validators import ValidationError

from base.models import Product
# Create your views here.
from base.serializers import ProductSerializer


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        name = self.request.data['name']
        product = Product.objects.filter(name=name)
        if product.exists():
            raise ValidationError("This Product already exists")
        serializer.save(user=user)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        product = Product.objects.get(name=self.request.data['name'])
        if self.request.data['image']:
            serializer.save(image=self.request.data['image'])
        else:
            serializer.save(image=product.image)
