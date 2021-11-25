from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import OwnerPermission
from .serializers import *
from rest_framework import generics


# Products
class ProductListView(APIView):
    """Общее описание продукции"""

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """Описание продукта"""

    def get(self, request, pk):
        products = Product.objects.get(id=pk)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)


# Reviews
class ReviewsView(APIView):
    """Все отзывы"""

    def get(self, request):
        query = Reviews.objects.all()
        serializer = ReviewsSerializer(query, many=True)
        print(request.session.session_key)
        return Response(serializer.data)


class ReviewsDetailView(APIView):
    """Вывод отзыва"""

    def get(self, request, pk):
        query = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(query)
        return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    """"Создание комментария"""

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [OwnerPermission, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """CRUD Комментариев"""

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [OwnerPermission]


# User
class UsersView(APIView):
    """Общее представление пользвателей"""
    permission_classes = [permissions.IsAdminUser]



    def get(self, request):
        query = User.objects.all()
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data)


class UsersDetailView(APIView):
    """Детальное представление пользователя"""

    def get(self, request, pk):
        query = User.objects.get(id=pk)
        serializer = UsersDetailSerializer(query)
        print(request.session)
        return Response(serializer.data)


# Cart
class CartView(APIView):
    """Общее представление всех существующих товаров в корзинах для авторизованого пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = CartProduct.objects.filter(owner=request.user)
        serializer = CartDetailSerializer(cart, many=True)
        return Response(serializer.data)


class CartDetailView(APIView):
    """Детальное представление товаров корзины"""

    def get(self, request, pk):
        cart = CartProduct.objects.get(id=pk)
        serializer = CartDetailSerializer(cart)
        return Response(serializer.data)


class CartCreateView(generics.CreateAPIView):
    """Добавление товаров в корзину. При добавлении товаров в корзину,
    сперва создается корзина для текущего пользователя, затем уже в неё добавляется товар"""

    queryset = CartProduct.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [OwnerPermission, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            Cart.objects.create(owner=User.objects.get(pk=self.request.user.pk))
        except:
            pass
        serializer.save(owner=Cart.objects.get(owner=self.request.user.pk))


class CartUpdateView(generics.UpdateAPIView):
    """Редактирование корзины"""

    queryset = CartProduct.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [OwnerPermission, permissions.IsAuthenticatedOrReadOnly]


# Order
class OrderView(APIView):
    """Общее представление всех существующих заказов"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    """Детальное представление заказа"""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    """Создание заказа и присваивание корзины текущего пользователя к заказу"""

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnerPermission]

    def perform_create(self, serializer):
        serializer.save(owner=Cart.objects.get(owner=User.objects.get(pk=self.request.user.pk)))


class OrderUpdateView(generics.UpdateAPIView):
    """Редактирование заказа"""

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [OwnerPermission]
