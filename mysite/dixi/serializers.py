from rest_framework import serializers

from .models import *


# Reviews
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewsParentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ('id', 'name', 'text', 'children')


# Products
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price', 'discount_bool', 'discount', 'new_price']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    material = serializers.SlugRelatedField(slug_field='name_model', read_only=True)
    reviews = ReviewsParentSerializer(many=True)
    price = PriceSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'amount', 'material', 'season', 'factory', 'size',
                  'gender', 'reviews']


# User
class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']


# Cart
class CartPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price']


class CartDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    products = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = '__all__'


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['products', 'amount']


# Order
class OrderSerializer(serializers.ModelSerializer):
    cart = CartDetailSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'delivery_address', 'description']
