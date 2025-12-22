from rest_framework.routers import DefaultRouter
from store.api.views import(
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet,
    CartViewSet,
    CartItemViewSet
)

router=DefaultRouter()
router.register("products",ProductViewSet, basename="products")
router.register("orders",OrderViewSet,basename="orders")
router.register("order-items",OrderItemViewSet,basename="order-items")
router.register("carts",CartViewSet,basename="carts")
router.register("cart-items",CartItemViewSet,basename="cart-items")

urlpatterns=router.urls
