from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product
# Create your views here.
from .serializers import ProductSerializer, MyTokenObtainPairSerializer, UserSerializer, UserSerializerWithToken


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

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializerWithToken

    def perform_create(self, serializer):
        data = self.request.data
        password = data['password']
        username = data['email']
        hashed_password = make_password(password)
        try:
            serializer.save(password=hashed_password, username=username)
        except:
            raise ValidationError({"message": 'User with this email already exists'}, code=status.HTTP_400_BAD_REQUEST)
        # user = User.objects.create(
        #     first_name=data['name'],
        #     username=data['email'],
        #     email=data['email'],
        #     password=make_password(data['password'])
        # )


class UserProfileAPIView(APIView):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        product = Product.objects.get(name=self.request.data['name'])
        image = product.image
        serializer.save(image=image)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
