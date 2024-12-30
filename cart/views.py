from django.shortcuts import render , redirect , get_object_or_404 , HttpResponse 
from store.models import Product
from .models import Cart_Item , Cart 
from store.models import Variation
from .utils import cart_id_
from django.urls import reverse
# Create your views here.
from django.core.exceptions import MultipleObjectsReturned
  

def add_cart(request, product_id):
    # جلب المنتج
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id_(request))  # الحصول على السلة أو إنشاؤها
    product_variation = []

    # معالجة التكرارات (مثل اللون والحجم) من الطلب
    if request.method == 'POST':
        #items here to get key and value together
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
                
            except Variation.DoesNotExist:
                pass

    # البحث عن العناصر الموجودة بنفس المنتج والتكرارات في السلة
    cart_items = Cart_Item.objects.filter(product=product, cart=cart)
    existing_cart_item = None

    for cart_item in cart_items:
        # مقارنة التكرارات باستخدام المجموعات (sets)
        # set here to range data
        existing_variations = set(cart_item.varitations.all())
        incoming_variations = set(product_variation)
        # if the data was sent and the data existing in cart item the same think
        if existing_variations == incoming_variations:
            #use existing cart item ka2nha cart_item
            existing_cart_item = cart_item
            
            break # إيقاف الحلقة لأننا وجدنا العنصر المتطابق

    if existing_cart_item:
        # زيادة الكمية إذا كان العنصر موجودًا بالفعل بنفس التكرارات
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # إنشاء عنصر جديد إذا لم يكن موجودًا
        new_cart_item = Cart_Item.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if product_variation:
            new_cart_item.varitations.set(product_variation)
        new_cart_item.save()

    return redirect('cart:cart_details')


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
        tax = (2 * total)    /100
        grand_total = tax + total
    except Cart.DoesNotExist:
        # If no cart exists, set cart_items to an empty queryset
        cart_items = []

    # Pass context data to the template
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total' : grand_total,
        'tax' : tax
    }

    return render(request, 'store_html/cart.html', context)


def remove_cart_item(request, product_id,cart_item_id):
    cart = get_object_or_404(Cart, cart_id=cart_id_(request))
    pro = get_object_or_404(Product, id=product_id)

    try:
        item = Cart_Item.objects.filter(product=pro, cart=cart , id =cart_item_id)
        item.delete()
    except Cart_Item.DoesNotExist:
        print("Cart_Item does not exist.")
    
    return redirect('cart:cart_details')


def mainus(request, product_id , cart_item_id):
    
    cart = get_object_or_404(Cart, cart_id=cart_id_(request))
    pro = get_object_or_404(Product, id=product_id)
    
   
    
    try:

            cart_item = Cart_Item.objects.filter(cart=cart , product = pro  , id = cart_item_id)
            for item in cart_item:
                if  item.quantity > 0:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
   
    except Cart_Item.DoesNotExist:
            print("No matching Cart_Item found.")
    
    return redirect('cart:cart_details')


