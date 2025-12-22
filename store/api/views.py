from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from store.models import Product,Order,Cart,CartItem,OrderItem
from .serializers import (
    ProductSerializer,
      OrderSerializer,
      CartSerializer,
      CartItemSerializer,
      OrderItemSerializer
)
class ProductViewSet(ReadOnlyModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]

class OrderViewSet(ReadOnlyModelViewSet):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        
        return(
         Order.objects.filter(
            customer__user=self.request.user)
         ).select_related("customer")

class OrderItemViewSet(ReadOnlyModelViewSet):
    serializer_class=OrderItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return( OrderItem.objects.filter(
            order__customer__user=self.request.user)

        ).select_related("order","product")
class CartViewSet(ReadOnlyModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return( Cart.objects.filter(
            customer__user=self.request.user)

        ).select_related("customer")

class CartItemViewSet(ReadOnlyModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return (CartItem.objects.filter(
         cart__customer__user=self.request.user)

             
        ).select_related("cart","product")











