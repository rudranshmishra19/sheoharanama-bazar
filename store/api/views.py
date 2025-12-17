from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from store.models import Product,Order,Cart,CartItem
from .serializers import ProductSerializer, OrderSerializer,CartSerializer,CartItemSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def product_list(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(["GET"])
def order_list(request):
    orders=Order.objects.all()
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cart(request):
    cart=Cart.objects.all()
    serializer=CartSerializer(cart,many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cartItem(request):
    cartItem=CartItem.objects.all()
    serializer=CartItemSerializer(cartItem,many=True)
    return Response(serializer.data)





