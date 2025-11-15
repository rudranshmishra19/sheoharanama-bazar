from django.contrib import admin
from .models import Category,Product,Customer,Order,OrderItem,Cart,CartItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)

class productAdmin(admin.ModelAdmin):
    list_display=('name','category','price','package_type','diet_type', 'weight', 'brand' )
    search_fields=('name','brand','category__name')
