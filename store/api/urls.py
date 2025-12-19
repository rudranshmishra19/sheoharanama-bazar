from django.urls import path
# from store.api.views import Cart,CartItem
from store.api.views import ProductListView, OrderListView,CartListView,CartItemListView
urlpatterns =[
    # path("products/",product_list,name="product-list"),
    # path("orders/",order_list,name="order-list"),
    
    path("carts/",CartListView.as_view(),name="cart-list"),
    path("cartitems/",CartItemListView.as_view(),name="cart-Item"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("orders/", OrderListView.as_view(), name="order-list"),
]
