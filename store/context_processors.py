# store/context_processors.py
from .models import Category
from .models import Customer

def categories_processor(request):
    categories=Category.objects.all()
    print(f"DEBUG:Context processor loaded{categories.count} categories")
    return {
        'categories':Category.objects.all() 
    }

def address_processor(request):
    """
    Context processor to add user address to all templates 
    """
    context={}
    if request.user.is_authenticated:
        try:
            #Get customer profile with address
            customer=Customer.objects.get(user=request.user)
            # handle if customer exist and the address is not updated 
            if customer.address:
                context['current_address']=customer.address
            else:
                context['current_address']=request.session.get('user_address','user,location')    
        
            context['current_address']=customer.address
        except Customer.DoesNotExist:
            #Fallback to session or default
            context['current_address']=request.session.get('user_address','user,location')

    else:
        #for non-authenticated users,use session or default 
        context['current_address']=request.session.get('user_address','user,location')

    return context 
