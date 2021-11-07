from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import *


class ProductListView(APIView):
    "Общее описание продукции"

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    'Описание продукта'

    def get(self, request, pk):
        products = Product.objects.get(id=pk)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)


class ReviewsView(APIView):
    'Все отзывы'

    def get(self, request):
        query = Reviews.objects.all()
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data)


class ReviewsDetailView(APIView):
    'Описание продукта'

    def get(self, request, pk):
        query = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(query)
        return Response(serializer.data)


class ReviewsCreateView(APIView):
    'Добавление отзыва'
    def post(self, request):
        review = ReviewsSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)