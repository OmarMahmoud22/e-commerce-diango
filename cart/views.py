from django.shortcuts import render , redirect , get_object_or_404
from store.models import Product
from .models import Cart_Item , Cart
from .utils import cart_id_
# Create your views here.
  

def add_cart(request, product_id):
    # Fetch the product
    product = get_object_or_404(Product, id=product_id)

    # Get or create the cart
    cart, created = Cart.objects.get_or_create(cart_id=cart_id_(request))

    # Get or create the cart item
    cart_item, created = Cart_Item.objects.get_or_create(product=product, cart=cart)
    if not created:
        # If the cart item already exists, increment the quantity
        cart_item.quantity += 1
    else:
        # If the cart item is new, set the quantity to 1
        cart_item.quantity = 1
    
    # Save the cart item
    cart_item.save()

    return redirect('cart_details')



def cart(request, total=0, quantity=0):
    try:
        # Get the current cart associated with the session
        cart = get_object_or_404(Cart, cart_id=cart_id_(request))
        
        # Get all active cart items for this cart
        cart_items = Cart_Item.objects.filter(cart=cart, is_active=True)
        
        # Calculate total price and quantity
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
    except Cart.DoesNotExist:
        # If no cart exists, set cart_items to an empty queryset
        cart_items = []

    # Pass context data to the template
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, 'store_html/cart.html', context)
