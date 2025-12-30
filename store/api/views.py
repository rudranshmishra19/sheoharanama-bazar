from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from store.models import Product,Order,Cart,CartItem,OrderItem,Category
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .serializers import (
    ProductSerializer,
      OrderSerializer,
      CartSerializer,
      CartItemSerializer,
      OrderItemSerializer,
      CatergorySerializer,
      FeaturedProductSerializer
)
class HomeApiView(APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        categories=Category.objects.all()
        featured_products=Product.objects.filter(available=True)[:3]

        category_data=CatergorySerializer(categories,many=True).data
        product_data=FeaturedProductSerializer(featured_products,many=True).data

        return Response({
            "categoires":category_data,
            "featured_products":product_data,
        })

class TrackPackage(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        orders=Order.objects.filter(
            customer__user=request.user
            )

        pending_orders=orders.filter(status__in=['pending','processing','shipped'])
        delivered_orders=orders.filter(status='delivered')
        cancelled_orders=orders.filter(status='cancelled')

        Pending_orders=OrderSerializer(pending_orders,many=True).data
        Delivered_orders=OrderSerializer(delivered_orders,many=True).data
        Cancelled_orders=OrderSerializer(cancelled_orders,many=True).data
       
        return Response({
            "pending_orders":Pending_orders,
            "delivered_orders":Delivered_orders,
            "cancelled_orders":Cancelled_orders,
        })
      
        
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
        
        # Fix Start
        try:
            quantity=int(quantity)
        except(TypeError,ValueError):
            raise ValidationError({"quantity":"Quantity must be a number"})    
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
            
        )    

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
    # To cancel the order 
    @action(detail=True, methods=["post"],)
    def cancel(self,request,pk=None):
        order=self.get_object()

        if order.status=="delivered":
               return Response(
               {"detail": "Delivered order cannot be cancelled"},
                 status=status.HTTP_403_FORBIDDEN
                )
        
        #2 already cancelled
        if order.status=="cancelled":
            return Response (
                {"detail": "Order is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # 3 Cancel the order 
        order.status="cancelled"
        order.save()

        return Response(
            {"message": "Order cancelled "},
            status=status.HTTP_200_OK
                        )
    @action(detail=True, 
            methods=["post"], 
            throttle_classes=[UserRateThrottle]
            )
    def example_adhoc_method(self,request, pk=None):
        return Response(
            {"status": "request was permitted"},
            status=status.HTTP_200_OK
        )
        
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













