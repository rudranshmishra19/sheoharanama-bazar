from rest_framework import serializers
from store.models import Product,Order,OrderItem,Customer,Cart,CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id"  ,"description" ,"price" , "image" ,"available"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=["id", "customer", "created_at", "updated_at", "completed"]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=["id","order","product","quantity","price"]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=["id", "customer", "created_at"]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=["id", "cart", "product" ,"quantity"]

