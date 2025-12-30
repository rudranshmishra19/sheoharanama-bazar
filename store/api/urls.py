from rest_framework.routers import DefaultRouter
from django.urls import path
from store.api.views import(
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet,
    CartViewSet,
    CartItemViewSet,
    HomeApiView,
    TrackPackage

)

router=DefaultRouter()
router.register("products",ProductViewSet, basename="products")
router.register("orders",OrderViewSet,basename="orders")
router.register("order-items",OrderItemViewSet,basename="order-items")
router.register("carts",CartViewSet,basename="carts")
router.register("cart-items",CartItemViewSet,basename="cartitems")

urlpatterns=[
    path("home/",HomeApiView.as_view(),name="home-api"),
    path("track/",TrackPackage.as_view(),name="track-api"),
]
urlpatterns+=router.urls
