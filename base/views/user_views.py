from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
from base.serializers import MyTokenObtainPairSerializer, UserSerializer, UserSerializerWithToken


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
