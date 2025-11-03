from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home_view,name='home'),
    path('home/',views.home_view,name='home'),
    path('list/',views.product_list,name='list'),
    path('category/<slug:category_slug>/',views.category_products,name='category_products'),
    path('cart/',views.cart_view,name='cart'),
    path('cart/add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/update/<int:item_id>/',views.update_cart_item,name='update_cart_item'),
    path('cart/remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('cart/clear/',views.clear_cart,name='clear_cart'),
    path('cart/increment/<int:item_id>/',views.increment_quantity,name='increment_quantity'),
    path('cart/decrement/<int:item_id>/',views.decrement_quantity,name='decrement_quantity'),
    path('login/',auth_views.LoginView.as_view(template_name='products/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='products/logout.html'),name='logout'),
    path('register/',views.register_view,name='register'),
    path('search/',views.search_view,name='search'),
    path('update_address/',views.update_address,name='update_address'),
    path('orders/',views.order_history,name='orders_history'),
    path('orders/return/',views.return_requests,name='return_requests'),
    path('orders/buy-again/',views.buy_again,name='buy_again'),
    path('track-package/',views.track_package,name='track_package'),
    path('orders/help',views.help,name='help'),
    
    
]

