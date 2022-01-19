from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .permissions import OwnerPermission
from .serializers import *
from .services import *


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
    """Create category"""

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class CategoryUpdateView(APIView):
    """Update category"""

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        queryset = Category.objects.get(id=pk)
        data = request.data
        queryset.name = data['name']
        queryset.save()
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)


class MaterialCreateView(APIView):
    """Create Material"""

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
    """
    Update product. You can change any fields
    from this list: ["title", "season", "factory", "slug"]
    """

    permission_classes = [permissions.IsAdminUser]

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
    """"Create size, amount for the product"""

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = SizeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class SizeUpdateView(APIView):
    """Update amount for the product"""

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
    """"
    Update price for the product.
    You can change any fields on this list: "discount", "price".
    If you cheng field "discount" field "new_price" will change automatically.
    """

    def put(self, request, pk):
        queryset = Price.objects.get(id=pk)
        data = request.data
        if 'price' in data:
            queryset.price = data['price']
        if 'discount' in data:
            queryset.discount = data['discount']
        queryset.new_price = Discount(queryset.price, queryset.discount).discount_price()
        queryset.save()
        serializer = PriceCreateSerializer(queryset)
        return Response(serializer.data)


# Reviews
class ReviewsView(APIView):
    """Get all Reviews"""

    def get(self, request):
        query = Reviews.objects.all()
        serializer = ReviewsSerializer(query, many=True)
        return Response(serializer.data)


class ReviewsDetailView(APIView):
    """Get one Review"""

    def get(self, request, pk):
        query = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(query)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """
    Create Review. After created review to the field "owner" assigned the user
    who created the comment.
    """

    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class ReviewUpdateView(APIView):
    """
    Update Review. Only the person who created comment can edit it.
    """
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
    """
    Get Users list
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        query = User.objects.all()
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data)


class UsersDetailView(APIView):
    """
    Get Detail User
    """

    def get(self, request, pk):
        query = User.objects.get(id=pk)
        serializer = UsersDetailSerializer(query)
        return Response(serializer.data)


# Cart
# class CartView(APIView):
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             cart = CartProduct.objects.filter(owner=Cart.objects.get(owner=request.user))
#         else:
#             cart = CartProduct.objects.filter(owner=Cart.objects.get(id=request.session['cart']))
#         serializer = CartDetailSerializer(cart, many=True)
#         return Response(serializer.data)


# class CartDetailView(APIView):
#     def get(self, request, pk):
#         cart = Cart.objects.get(id=pk)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)


class CartCreateView(APIView):
    """
    After adding an item to the cart. First, a shopping cart is created, then the goods are placed in it.
    If the user adds an already existing product to the cart, then the quality of the product is increased by 1.
    The price increases as the amount of items in the cart increases.
    """

    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartCreateSerializer(data=request.data)
        data = request.data
        GetOrCreateCart(request.user).get_or_create_cart()
        if CheckDuplicateProduct(request.user, data['product']).check_duplicate_product_in_cart():
            if serializer.is_valid():
                instance = serializer.save(price=TotalPrice(data['product'], data['amount']).get_total_price())
                instance.owner = GetOrCreateCart(request.user).get_or_create_cart()
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.is_valid():
                DuplicateFinded(request.user, data['product'], data['amount']).duplicate_finded()
        return Response(serializer.errors)


class CartUpdateView(APIView):
    """
    Update CartProduct.
    When editing a cart, only one field is available - "amount".
    """

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
    """
    Show Orders List.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    """
    Detail view of one order.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderCreateView(APIView):
    """
    Create Order.
    When placing an order, the total amount of all items in the cart is calculated.
    Data with the contents of the order is sent to the seller's mail.
    An entity is also created in the database in which data about the purchased product,
    its size and quantity are placed.
    Then the entire contents of the basket are cleared.
    """
    permission_classes = [OwnerPermission, permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save(owner=GetOrCreateCart(request.user).get_or_create_cart())
            instance.final_price = OrderTotalPrice(request.user).get_total_price_all_cartproduct()
            instance.save()
            CreateOrderDetail(request.user, instance).create_order_detail()
            SendMailSalesman(instance).send_mail_after_order()
            CleanCart(request.user).clean_cart()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class OrderUpdateView(APIView):
    """
    Edit Order.
    When editing an order, you can change the following fields: "first_name", "last_name", "phone_number",
    "delivery_address", "description".
    """

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        queryset = Order.objects.get(id=pk)
        data = request.data
        if 'first_name' in data:
            queryset.first_name = data['first_name']
        if 'last_name' in data:
            queryset.last_name = data['last_name']
        if 'phone_number' in data:
            queryset.phone_number = data['phone_number']
        if 'delivery_address' in data:
            queryset.delivery_address = data['delivery_address']
        if 'description' in data:
            queryset.delivery_address = data['description']
        queryset.save()
        serializer = OrderCreateSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GalleryCreateView(APIView):
    """
    Adding an image to a product.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class CreateProductPrice(APIView):

    def post(self, request):
        data = request.data
        product_serializer = SuperSerializer(data=data)
        if product_serializer.is_valid():
            CreateProductService(data).fill_product()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors)
