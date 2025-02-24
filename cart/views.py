from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
    
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
        cart_items = Cart_Item.objects.filter(product=product, user=current_user)
        existing_cart_item = None

        for cart_item in cart_items:
            # مقارنة التكرارات باستخدام المجموعات (sets)
            # set here to range data
            existing_variations = set(cart_item.varitations.all())
            incoming_variations = set(product_variation)
            # if the data was sent and the data existing in cart item the same think
            if existing_variations == incoming_variations:
                #use existing cart item ka2nha cart_item عشان في اتنين شبه بعض
                existing_cart_item = cart_item

                break # إيقاف الحلقة لأننا وجدنا العنصر المتطابق

        if existing_cart_item:
            if product.stock >= existing_cart_item.quantity + 1:
            # زيادة الكمية إذا كان المخزون يسمح بذلك
              existing_cart_item.quantity += 1
              existing_cart_item.save()
            else:
            # عرض رسالة أو التعامل مع الحالة إذا كان المخزون غير كافٍ
                messages.error(request, "لا يمكن زيادة الكمية لأن المخزون غير كافٍ.")
            # زيادة الكمية إذا كان العنصر موجودًا بالفعل بنفس التكرارات
        else:
        # التحقق من المخزون قبل إنشاء عنصر جديد
            if product.stock >= 1:
            # إنشاء عنصر جديد إذا كان المخزون يسمح بذلك
                new_cart_item = Cart_Item.objects.create(
                product=product,
                user=current_user,
                quantity=1
                )
            if product_variation:
                new_cart_item.varitations.set(product_variation)
                new_cart_item.save()
            else:
            # التعامل مع حالة عدم توفر مخزون كافٍ
                messages.error(request, "لا يمكن إضافة المنتج لأن المخزون غير متوفر.")
        return redirect('cart:cart_details')
    else:
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
                #use existing cart item ka2nha cart_item عشان في اتنين شبه بعض
                existing_cart_item = cart_item

                break # إيقاف الحلقة لأننا وجدنا العنصر المتطابق

        if existing_cart_item:
            if product.stock >= existing_cart_item.quantity + 1:
            # زيادة الكمية إذا كان المخزون يسمح بذلك
              existing_cart_item.quantity += 1
              existing_cart_item.save()
            else:
            # عرض رسالة أو التعامل مع الحالة إذا كان المخزون غير كافٍ
                messages.error(request, "لا يمكن زيادة الكمية لأن المخزون غير كافٍ.")
            # زيادة الكمية إذا كان العنصر موجودًا بالفعل بنفس التكرارات
        else:
        # التحقق من المخزون قبل إنشاء عنصر جديد
            if product.stock >= 1:
            # إنشاء عنصر جديد إذا كان المخزون يسمح بذلك
                new_cart_item = Cart_Item.objects.create(
                product=product,
                cart=cart,
                quantity=1
                )
            if product_variation:
                new_cart_item.varitations.set(product_variation)
                new_cart_item.save()
            else:
            # التعامل مع حالة عدم توفر مخزون كافٍ
                messages.error(request, "لا يمكن إضافة المنتج لأن المخزون غير متوفر.")
        return redirect('cart:cart_details')


def cart(request, total=0, quantity=0):
    try:
        if request.user.is_authenticated:
        # Get the current cart associated with the session
            cart_items = Cart_Item.objects.filter(user=request.user, is_active=True)
        else:    
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

    return render(request, 'store/cart.html', context)


def remove_cart_item(request, product_id,cart_item_id):
    
    try:
        current_user = request.user
        pro = get_object_or_404(Product, id=product_id)

        if current_user.is_authenticated:
            item = Cart_Item.objects.get(product=pro, user=current_user , id =cart_item_id)
            item.delete()   
        else:    
            cart = get_object_or_404(Cart, cart_id=cart_id_(request))
            item = Cart_Item.objects.get(product=pro, cart=cart , id =cart_item_id)
            item.delete()
    except Cart_Item.DoesNotExist:
        print("Cart_Item does not exist.")
    
    return redirect('cart:cart_details')


def mainus(request, product_id , cart_item_id):
    current_user = request.user
    
    pro = get_object_or_404(Product, id=product_id)
    try:  
            if current_user.is_authenticated:
                cart_item = Cart_Item.objects.get(user=current_user , product = pro  , id = cart_item_id)
            else:
                cart = get_object_or_404(Cart, cart_id=cart_id_(request))
                cart_item = Cart_Item.objects.get(cart=cart , product = pro  , id = cart_item_id)
                
            if  cart_item.quantity > 0:
                    cart_item.quantity -= 1
                    cart_item.save()
            else:
                    cart_item.delete()
   
    except Cart_Item.DoesNotExist:
            print("No matching Cart_Item found.")
    
    return redirect('cart:cart_details')

@login_required(login_url='login')
def check_out(request, total=0, quantity=0,cart_items=None):
    
    try:
        if request.user.is_authenticated:
        # Get the current cart associated with the session
            cart_items = Cart_Item.objects.filter(user=request.user, is_active=True)
        # Get the current cart associated with the session
        else:
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
 
    return render(request , 'store/check_out.html' , context)