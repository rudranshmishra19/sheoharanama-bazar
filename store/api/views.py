from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from store.models import Product,Order,Cart,CartItem,OrderItem
from .serializers import ProductSerializer, OrderSerializer,CartSerializer,CartItemSerializer,OrderItemSerializer

class ProductListView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]

class OrderListView(ListAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            customer__user=self.request.user

        ).select_related("customer")

class OrderItemListView(ListAPIView):
    serializer_class=OrderItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(
            Order__customer__user=self.request.user

        ).select_related("order","product")
class CartListView(ListAPIView):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(
            customer__user=self.request.user

        ).select_related("customer")

class CartItemListView(ListAPIView):
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
         cart__customer__user=self.request.user

             
        ).select_related("cart","product")









