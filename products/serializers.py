from rest_framework import serializers
from .models import Products, BillingAddress, Order, OrderedItem, Favourites
from categories.models import Category
from .models import Shops
from .models import ProductRatings
from django.contrib.auth.models import User
from customers.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    shop = ShopsSerializer()
    class Meta:
        model = Products
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ProductRatingsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()
    class Meta:
        model = ProductRatings
        fields = '__all__'


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    billing_address = BillingAddressSerializer()
    class Meta:
        model = Order
        fields = '__all__'


class OrderedItemSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    class Meta:
        model = OrderedItem
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    user = UserSerializer()
    class Meta:
        model = BillingAddress
        fields = '__all__'
