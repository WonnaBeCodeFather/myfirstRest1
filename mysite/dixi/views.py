from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import OwnerPat
from .serializers import *
from rest_framework import generics


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
    'Вывод отзыва'

    def get(self, request, pk):
        query = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(query)
        return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [OwnerPat, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [OwnerPat]
