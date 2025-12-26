from rest_framework import serializers
from store.models import Product,Order,OrderItem,Customer,Cart,CartItem,Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id"  ,"description" ,"price" , "image" ,"available"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
        read_only_fields=["id", "customer", "created_at", "updated_at", "status"]

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
        fields="__all__"
        read_only_fields=["cart"]

# Category serializer
class CatergorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id", "name"] #add fields as needed

# Featured products
class FeaturedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","price","image"]



