from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .permissions import OwnerPermission
from .serializers import *
from .services import *
from django.db import transaction


# Products
class ProductListView(APIView):
    """Get all products"""

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """Get one product"""

    def get(self, request, slug):
        products = Product.objects.get(slug=slug)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)


class CategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class CategoryUpdateView(APIView):
    def put(self, request, pk):
        snippet = Category.objects.get(id=pk)
        data = request.data
        snippet.name = data['name']
        snippet.save()
        serializer = CategorySerializer(snippet)
        return Response(serializer.data)


class MaterialCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


# class ProductCreateView(APIView):
#     def post(self, request):
#         serializer = ProductCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors)


class ProductUpdateView(APIView):
    def put(self, request, pk):
        queryset = Product.objects.get(id=pk)
        data = request.data
        if 'title' in data:
            queryset.name = data['title']
        if 'season' in data:
            queryset.season = data['season']
        if 'factory' in data:
            queryset.factory = data['factory']
        if 'slug' in data:
            queryset.slug = data['slug']
        queryset.save()
        serializer = ProductListSerializer(queryset)
        return Response(serializer.data)


class SizeCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = SizeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class SizeUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        queryset = Size.objects.get(id=pk)
        data = request.data
        queryset.amount = data['amount']
        queryset.save()
        serializer = SizeCreateSerializer(queryset)
        return Response(serializer.data)


# Price
# class PriceCreateView(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = PriceCreateSerializer(data=data)
#         if serializer.is_valid():
#             instance = serializer.save()
#             instance.new_price = PriceService().discount_price(instance.price, instance.discount)
#             instance.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)


class PriceUpdateView(APIView):
    def put(self, request, pk):
        queryset = PriceService(pk).get_product_price
        data = request.data
        if 'price' in data:
            queryset.price = data['price']
        if 'discount' in data:
            queryset.discount = data['discount']
        queryset.new_price = PriceService(pk).discount_price(queryset.price, queryset.discount)
        queryset.save()
        serializer = PriceCreateSerializer(queryset)
        return Response(serializer.data)


# Reviews
class ReviewsView(APIView):

    def get(self, request):
        query = Reviews.objects.all()
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data)


class ReviewsDetailView(APIView):

    def get(self, request, pk):
        query = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(query)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class ReviewUpdateView(APIView):
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def put(self, request, pk):
        queryset = Reviews.objects.get(id=pk)
        data = request.data
        queryset.text = data['text']
        queryset.save()
        serializer = ReviewsSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk):
        queryset = Reviews.objects.get(id=pk)
        queryset.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


# User
class UsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        query = User.objects.all()
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data)


class UsersDetailView(APIView):

    def get(self, request, pk):
        query = User.objects.get(id=pk)
        serializer = UsersDetailSerializer(query)
        return Response(serializer.data)


# Cart
class CartView(APIView):

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


class CartCreateView(APIView):
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartCreateSerializer(data=request.data)
        data = request.data
        CartProductService(request.user)
        if CartProductService(request.user).check_duplicate_product_in_cart(data['product']):
            if serializer.is_valid():
                instance = serializer.save(price=PriceService(data['product']).get_total_price(data['amount']))
                instance.owner = CartProductService(request.user).cart_queryset_user
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            CartProductService(request.user).duplicate_finded(data['product'], data['amount'])
        return Response(serializer.errors)


class CartUpdateView(APIView):
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def put(self, request, pk):
        queryset = CartProduct.objects.get(id=pk)
        data = request.data
        queryset.amount = data['amount']
        queryset.save()
        serializer = CartCreateSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk):
        queryset = CartProduct.objects.get(id=pk)
        queryset.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


# Order
class OrderView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


@transaction.atomic
class OrderCreateView(APIView):
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save(owner=CartProductService(request.user).cart_queryset_user)
            instance.final_price = OrderService(request.user).get_total_price_all_cartproduct()
            instance.save()
            OrderService(request.user).set_order_for_order_product(instance)
            OrderService(request.user).send_mail_after_order(instance)
            CartProductService(request.user).clean_cartproduct()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class OrderUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        queryset = Order.objects.get(id=pk)
        data = request.data
        queryset.first_name = data['first_name']
        queryset.last_name = data['last_name']
        queryset.phone_number = data['phone_number']
        queryset.delivery_address = data['delivery_address']
        queryset.save()
        serializer = OrderCreateSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class SuperView(APIView):

    def post(self, request):
        data = request.data
        product_serializer = SuperSerializer(data=data)
        if product_serializer.is_valid():
            SuperService(data).main()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors)
