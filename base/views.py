from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Product
# Create your views here.
from .serializers import ProductSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>>/reviews/',
        '/api/products/top/',
        '/api/products/<id>/',
        '/api/products/delete/<id>/',
        '/api/products/<update>/<id>/',
    ]
    return Response(routes)


# @api_view(['GET'])
# def getProducts(request):
#     return Response(products)

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


# @api_view(['GET'])
# def getProduct(request, pk):
#     product = {}
#     for prod in products:
#         if prod['_id'] == pk:
#             product = prod
#             break
#
#     return Response(product)

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        product = Product.objects.get(name=self.request.data['name'])
        image = product.image
        serializer.save(image=image)
