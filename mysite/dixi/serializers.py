import requests_oauthlib
from rest_framework import serializers

from .models import *


# Reviews
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        exclude = ['owner']


class FilterReviewsListSerializer(serializers.ListSerializer):
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
        list_serializer_class = FilterReviewsListSerializer
        model = Reviews
        fields = ('id', 'name', 'text', 'children')


# Products
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price', 'discount_bool', 'discount', 'new_price']


class PriceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    material = serializers.SlugRelatedField(slug_field='name_model', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    material = serializers.SlugRelatedField(slug_field='name_model', read_only=True)
    reviews = ReviewsParentSerializer(many=True)
    gender = serializers.CharField(source='get_gender_display')
    season = serializers.CharField(source='get_season_display')
    price = PriceSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'amount', 'material', 'season', 'factory', 'size',
                  'gender', 'reviews']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


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
    products = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product = CartDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['products', 'amount']


# Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['id', 'owner']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['final_price'] = ret['final_price'] + ' грн'
        return ret


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'delivery_address', 'description']
