from django.shortcuts import render,get_object_or_404,redirect
from .models import Category, Product, Cart,CartItem,Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order,Product,OrderItem
from django.db.models import Q

# Category views
def category_products(request,category_slug):
    """
     Display products for a specific category
    """
    category=get_object_or_404(Category,slug=category_slug)
    products=Product.objects.filter(category=category,avaiable=True)

    context={
        'category':category,
        'products':products,
    }
    return render(request,'products/category_products.html',context)


def test_categories(request):
    return render(request, 'base.html')

def home_view(request):
    """Home page with dynamic categories"""
    categories=Category.objects.all() #Get all categories from database
    featured_products=Product.objects.filter(available=True)[:6]  #frist 6 products

    #Get address from session or use default
   
    """Home page"""

    context={
        'categories':categories, #This will be used in navigation 
        'featured_products':featured_products,
       

                                                              
    }
    return render(request,'products/home.html',context)

@login_required
def order_history(request):
    """Display user's order histoty"""
    try:
        customer=request.user.customer
        orders=Order.objects.filter(customer=customer).prefetch_related('item_product')
    except:
        orders=[]
    context={'orders': orders}
    return render(request,'orders/history.html',context)
         
@login_required
def return_requests(request):
    """Display return requests page """
    context={}
    return render(request,'orders/returns.html',context)

@login_required
def buy_again(request):
    """Show produts user previously purchased"""
    try:
        customer=request.user.customer
        purchased_products=Product.objects.filter(
            orderitem_order_customer=customer
        ).distinct()
    except:
        purchased_products=[]
    context={'products':purchased_products}
    return render(request,'orders/buy_again.html',context)
        
def product_list(request):
    """All products page"""
    try:

        categories=Category.objects.all()
        products=Product.objects.filter(available=True)

        context={
           'categories':categories,
            'products':products,
            'featured_products':products[:4] 


       } 
        return render(request,'products/list.html',context)
    except Exception as e:
        #Handle exeption 
        return render(request,'error.html',{'error':str(e)})

def track_package(request):
    """Track all the packages """
    try:
        customer=request.user.customer
        # Get all orders
        orders=Order.objects.filter(customer=customer).prefetch_related('orderitem_set').order_by('-created_at')
        #Organize orders by status for better display
        pending_orders=orders.filter(status__in=['pending','processing','shipped'])
        delivered_orders=orders.filter(status='delivered')
        cancelled_orders=orders.filter(status='cancelled')


        context={
            'pending_orders':pending_orders,
            'delivered_orders':delivered_orders,
            'cancelled_orders':cancelled_orders,
            'total_orders':orders.count(),
            'active_orders':pending_orders.count(),
        }
    except Exception as e:
        #Handle case where user doesnt have customer profile
        context={
            'error':'Unable to load order tracking information',
            'pending_orders':[],
            'delivered_orders':[],
            'cancelled_orders':[],
            'total_orders':0,
            'active_orders':0,
        }

    return render(request,'orders/track_package.html',context)

def help(request):
    "Simple view to render help page"
    return render(request,'orders/help.html')


def register_view(request):
    if request.method=='POST': #User submitted the from 
        form=UserCreationForm(request.POST) #Form with user data
        if form.is_valid():
            form.save()
            return redirect('login') #Redirect to login page 
    else:
        form=UserCreationForm() #Empty form 

    return render(request,'products/register.html',{'form':form})

def update_address(request):
    if request.method=='POST':
        #Get form data
        full_name=request.POST.get('full_name')
        mobile=request.POST.get('mobile')
        pincode=request.POST.get('pincode')
        address_line1=request.POST.get('address_line1')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        state=request.POST.get('state')
        default_address=request.POST.get('default_address')
        instructions=request.POST.get('instructions')
        
        # string to display address
        address_display=f"{full_name},{city},-{pincode}"
        

        #Also store individual fields in session for pre-filling the form later
        request.session['address_data']={
            'full_name':full_name,
            'mobile':mobile,
            'pincode':pincode,
            'address_line1':address_line1,
            'landmark':landmark,
             'city':city,
             'state':state,
             'default_address':default_address,
             'instructions':instructions,
        } 
        #save to session
        request.session['user_address']=address_display

        #Also save to Customer model if user is authenticated 
        if request.user.is_authenticated:
            try:
                customer=Customer.objects.get(user=request.user)
                customer.address=address_display
                #Also save phone if needed
                if mobile:
                    customer.phone=mobile
                customer.save()
            except Customer.DoesNotExist:
                #Create new customer profile
                customer=Customer.objects.create(
                    user=request.user,
                    address=address_display,
                    phone=mobile if mobile else ''
                )
        #Redirect back to home
        return redirect('home')
    #For Get request -pre fill from with existing data
    address_data=request.session.get('address_data',{})


    return render(request,'products/update_address.html',{
        'full_name': address_data.get('full_name', ''),
        'mobile': address_data.get('mobile', ''),
        'pincode': address_data.get('pincode', ''),
        'address_line1': address_data.get('address_line1', ''),
        'landmark': address_data.get('landmark', ''),
        'city': address_data.get('city', ''),
        'state': address_data.get('state', ''),
        'default_address': address_data.get('default_address', ''),
        'instructions': address_data.get('instructions', '')
    })



def search_view(request):
    #Get search parameters from the form 
    search_query=request.GET.get('q', '') #from input name="q"
    category_id=request.GET.get('category','') #from select name="category"

    # Start with All products from database
    products= Product.objects.all()
     #Get address from session or use default
  
    #Then FILTER based on user input:
    if search_query:
        products=products.filter(
            name__icontains=search_query
        )
    #Apply category filter if category selected 
    if category_id:
        products=products.filter(category_id=category_id)

    context={
        'products':products,
        'search_query':search_query,
        'selected_category':category_id,
        
    }        
    
    return render(request,'products/list.html',context) #using product_list as temporary html page 



@login_required
def cart_view(request):
    """
    Display the user's cart with all items and totals
    """
    try:
        # Get or create customer profile for the user
        customer,created=Customer.objects.get_or_create(user=request.user)
        if created:
            messages.success(request,"Welcome! Your customer profile was created .")
            
        else:
            # Customer already exits
            messages.info(request,f"Welcome back,{customer.user.username}!")
            
        # Get or create cart for the customer
        cart,cart_created=Cart.objects.get_or_create(customer=customer)

        if cart_created:
            messages.info(request,"cart created successfully")
    

        cart_items=cart.items.all()

        context={
            'cart':cart,
            'cart_items':cart_items,
            'total_items':cart.total_items,
            'total_price':cart.total_price,
            'page_title':'Your Shopping cart'
        }
        return render(request,'products/cart.html',context)
    
    except Exception as e:
        messages.error(request, f"Error loading cart: {str(e)}")
        return render(request, 'products/cart.html', {'cart_items': []})
    
@login_required
def add_to_cart(request,product_id):
    """
      Add a product to the cart or increase quantity if already exists
    """
    try:
        product=get_object_or_404(Product,id=product_id,available=True)
        # Get customer and cart
        customer=get_object_or_404(Customer,user=request.user)
        cart,created=Cart.objects.get_or_create(customer=customer)

        # Check if product already exists in cart
        cart_item,item_created=CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not item_created:
            # Item already exists,increase quantity
            cart_item.quantity+=1
            cart_item.save()
            message= f"Increased quantity of {product.name} in cart"
        else:
            # New item added
            message=f"{product.name} added to cart successfully!"

        message=f"{product.name} added to cart sucessfully !"

        # Redirect back to previous page or product list
        next_page=request.Meta.get('HTTP_REFERER','product_list')
        return redirect(next_page)
    except Exception as e:
        message.error(request,f"Error adding product to cart:{str(e)}") 
        return redirect ('product_list')

@login_required
def update_cart_item(request,item_id):
    
    try:
        cart_item=get_object_or_404(CartItem,id=item_id,cart__customer__user=request.user)

        if request.method=='POST':
            quantity=request.POST.get('quantity')

            if quantity and quantity.isdigit():
                quantity=int(quantity)

                if quantity>0:
                    cart_item.quantity=quantity
                    cart_item.save()
                    messages.success(request,"Cart updated sucessfully !")
                else:
                    #Remove item if quantity is 0
                    cart_item.delete()
                    messages.success(request,"Item removed from cart!")
            else:
                messages.error(request,"please enter a valid quantity")

        return redirect('cart_view')
    except Exception as e:
        messages.error(request,f"Error updating cart:{str(e)}")
        return redirect('cart_view')

@login_required
def remove_from_cart(request,item_id):
    """
    Remove an item completely from the chart
    """
    try:
        cart_item=get_object_or_404(CartItem,id=item_id,cart__customer__user=request.user)
        product_name=cart_item.product.name
        cart_item.delete()
        messages.success(request,f"{product_name} removed from cart!")
        return redirect('cart_view')
    
    except Exception as e:
        messages.error(request,f"Error removing item from cart:{str(e)}")
        return redirect('cart_view')

@login_required
def clear_cart(request):
    """
    Remove all items from the cart
    """    
    try:
        customer=get_object_or_404(Customer,user=request.user)
        cart=get_object_or_404(Cart,customer=customer)

        #Delete all cart items
        cart.items.all().delete()

        messages.success(request,"Cart cleared sucessfully !")
        return redirect('cart_view')
    
    except Exception as e:
        messages.error(request,f"Error clearning cart:{str(e)}")
        return redirect('cart_view')
    
@login_required
def increment_quantity(request,item_id):
    """
    Increase quantity of a cart item by 1
    """
    try:
        cart_item=get_object_or_404(CartItem,id=item_id,cart__customer__user=request.user)
        cart_item.quantity+=1
        cart_item.save()

        messages.success(request,"Quantity increased!")
        return redirect('cart_view')

    except Exception as e:
        messages.error(request,f"Error increasing quantity:{str(e)}")
        return redirect('cart_view')

@login_required
def decrement_quantity(request,item_id):
    """
    Decrease quantity of a cart item by 1,remove if quantity becomes 0
    """
    try:
        cart_item=get_object_or_404(CartItem,id=item_id,cart__customer__user=request.user)

        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
            messages.success(request,"Quantity decreased!")
        else:
            product_name=cart_item.product.name
            cart_item.delete()
            messages.success(request,f"{product_name} remove from cart!")

        return redirect('cart_view')

    except Exception as e:
        messages.error(request,f"Error decreasing  quantity:{str(e)}")
        return redirect('cart_view')

#Helper function to get cart summary()
def get_cart_summary(request):
    """
    Return cart summary for displaying in templates
    """
    if request.user.is_authenticated:
        try:
            customer=Customer.objects.get(user=request.user)
            cart=Cart.objects.filter(customer=customer).first()
            if cart:
                return{
                    'cart_total_items':cart.total_items,
                    'cart_total_price':cart.total_price
                }
        except (Customer.DoesNotExist,Cart.DoesNotExist):
            pass
    return {'cart_total_items':0, 'cart_total_price':0}
        



     
    
    

                        



   



