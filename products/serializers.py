from rest_framework import serializers
from .models import Products, BillingAddress
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Products
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product = CategorySerializer()
    class Meta:
        model = Products
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = BillingAddress
        fields = '__all__'