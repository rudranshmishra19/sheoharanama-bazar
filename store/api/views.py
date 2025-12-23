from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from store.models import Product,Order,Cart,CartItem,OrderItem
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

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

class OrderViewSet(ModelViewSet):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        
        return(
         Order.objects.filter(
            customer__user=self.request.user)
         ).select_related("customer")

    def perform_create(self, serializer):
        
        product_id=self.request.data.get("product")
        quantity=self.request.data.get("quantity",1)
        
        if not product_id:
            raise ValidationError({"product" :"Product is required"})
        
        if quantity<=0:
            raise ValidationError({"quantity": "Quantity must be greater than 0"})
        
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"product":"Invalid product"})
            
        order=serializer.save(
            customer=self.request.user.customer,
            status="placed",
            payment_method="COD",
            completed=False
        )    

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
    # To cancel the order 
    @action(detail=True, methods=["post"])
    def cancel(self,request,pk=None):
        order=self.get_object()

        if order.completed:
            raise ValidationError("Completed order cannot be cancelled")

        order.status= "cancelled"
        order.save()
        return Response({"message": "Order cancelled "})
        
        


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

class CartItemViewSet(ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return (CartItem.objects.filter(
         cart__customer__user=self.request.user)

             
        ).select_related("cart","product")
    
    def perform_create(self, serializer):
        cart=Cart.objects.get(customer__user=self.request.user)
        serializer.save(cart=cart)













