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

    def get(self, request, slug):
        products = Product.objects.get(slug=slug)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class PriceCreateView(generics.CreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceCreateSerializer


class PriceUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceCreateSerializer


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
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

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
        return Response(serializer.data)


# Cart
class CartView(APIView):
    """Общее представление всех существующих товаров в корзине пользователя"""

    def get(self, request):
        if request.user.is_authenticated:
            cart = CartProduct.objects.filter(owner=Cart.objects.get(owner=request.user))
        else:
            cart = CartProduct.objects.filter(owner=Cart.objects.get(id=request.session['cart']))
        serializer = CartDetailSerializer(cart, many=True)
        return Response(serializer.data)


class CartDetailView(APIView):
    def get(self, request, pk):
        cart = Cart.objects.get(id=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartCreateView(generics.CreateAPIView):
    """Добавление товаров в корзину. При добавлении товаров в корзину,
    сперва создается корзина для текущего пользователя, затем уже в неё добавляется товар"""

    queryset = CartProduct.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [OwnerPermission]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            try:
                Cart.objects.create(owner=User.objects.get(pk=self.request.user.pk))
            except:
                pass
            serializer.save(owner=Cart.objects.get(owner=self.request.user.pk))
        elif 'cart' not in self.request.session:
            get_pk = Cart.objects.create().pk
            obj = serializer.save(owner=Cart.objects.get(id=get_pk))
            self.request.session['cart'] = get_pk
        else:
            serializer.save(owner=Cart.objects.get(id=self.request.session['cart']))


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

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    """Создание заказа и присваивание корзины текущего пользователя к заказу"""

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [OwnerPermission]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=Cart.objects.get(owner=User.objects.get(pk=self.request.user.pk)))
        else:
            obj = serializer.save(owner=Cart.objects.get(id=self.request.session['cart']))
            obj.owner = Cart.objects.get(id=self.request.session['cart'])


class OrderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAdminUser]
