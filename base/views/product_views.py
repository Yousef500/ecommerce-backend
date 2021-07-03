from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from base.models import Product, Review
# Create your views here.
from base.serializers import ProductSerializer


class ProductListAPIView(ListCreateAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # pagination_class = ProductSetPagination

    # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        query = self.request.query_params.get('keyword')
        if query:
            products = Product.objects.filter(name__icontains=query)
        else:
            products = Product.objects.all()
        return products

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save(user=user)
        else:
            raise ValidationError(
                {'detail': 'You are not authorized to create products'},
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

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')
