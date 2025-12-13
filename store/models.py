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
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='products/default.png')
   

    # Dynamic features
    package_type =models.CharField(max_length=100,blank=True,null=True)
    diet_type=models.CharField(max_length=100,blank=True,null=True)
    item_form=models.CharField(max_length=100,blank=True,null=True)
    weight=models.CharField(max_length=100, blank=True,null=True)
    speciality=models.CharField(max_length=200, blank=True, null=True)
    brand=models.CharField(max_length=100, blank=True, null=True)


    #Quantity field
    quantity =models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        help_text="Numeric quantity (e.g 1.5 for 1.5kg or 2 for 2 pieces )"
    )
    #Unit field
    UNIT_CHOICES =[
        ('pcs', 'pieces'),
        ('g','Grams'),
        ('kg','Kilograms'),
        ('ml','Millilitres'),
        ('ltr','Litres'),
        ('pkt','Packet'),
        ('jar','Jar'),

    ]
    unit=models.CharField(max_length=10,choices=UNIT_CHOICES,default='pcs')

    
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
    status= models.CharField(
        max_length=20,
        choices=[
            ("placed","Placed"),
            ("shipped","Shipped"),
            ("out_for_delivery","OUt For Delivery"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        default="placed"
    )
    payment_method =models.CharField(max_length=10, default="COD")
    def __str__(self):
        return f"Order{self.id} by {self.customer}"


#OrderItem model (products in an order )
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=1)
    price =models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        #Decimal *int ->deciaml
        return self.price * self.quantity
    

#Cart model
class Cart(models.Model):
    customer=models.OneToOneField(Customer,on_delete=models.SET_NULL,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.customer and self.customer.user:
            return f"Cart of {self.customer.user.username}"
        return f"Cart #{self.id}"
    

    @property
    def total_items(self):
        return sum (item.quantity for item in self.items.all())

    @property
    def total_price(self):
        total =0 
        for item in self.items.all():
            if item.product and item.product.price is not None:
                total +=item.product.price *item.quantity
        return total        


#CartItem model
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items') 
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        # Handle case where product might be None
        if self.product:
              return f"{self.quantity} x {self.product.name}"
        else:
            return f"{self.quantity} x [Deleted Product ] (ID: {self.id})" 
    
    @property
    def total_price(self):
        # Handle case where product might be None
        if self.product and self.product.price:
            return self.product.price *self.quantity
        else:
            return 0  #return None,depending on your preference
        
        
    
    
     
    
    


    
       
    
    

        

