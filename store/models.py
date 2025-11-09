from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)


    def __str__(self):
        return self.name

#Product
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='proudcts/default.png')
    
    def __str__(self):
        return self.name

#Customer Class
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,blank=True)
    address=models.TextField(blank=True)

    def __str__(self):
        return self.user.username

#Order model
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return f"Order{self.id} by {self.customer}"

#OrderItem model (products in an order )
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

#Cart model
class Cart(models.Model):
    customer=models.OneToOneField(Customer,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.customer.user.username}"

    @property
    def total_items(self):
        return sum (item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum (item.product.price * item.quantity for item in self.items.all() )

#CartItem model
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items') 
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.product.price *self.quantity
    
    
     
    
    


    
       
    
    

        

