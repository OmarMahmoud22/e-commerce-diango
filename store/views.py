
from django.shortcuts import render , get_object_or_404
from .models import Product , Category
from cart.models import Cart_Item,Cart
from cart.utils import cart_id_
# Create your views here.

def home(request , cat_slug=None):
    cat = None
    pro = None
    if cat_slug != None :
        #if the user click the the link send to request
        cat = get_object_or_404(Category , slug = cat_slug)
        # get slug of catengury
        pro = Product.objects.filter(category=cat , is_available = True )
        # filter the products with the categury and available product
        product_count = pro.count()
    else :    
        # if  you dont clicked give me products available
        pro = Product.objects.all().filter(is_available = True)
        product_count = pro.count()

    context = {
        'products' : pro,
        'product_count' : product_count

        }
    return render(request , 'store_html/home.html' , context)


def product_detail(request, cat_slug, slug_product):
    try:
        pro = get_object_or_404(Product , category__slug = cat_slug   ,slug=slug_product)
        in_cart = Cart_Item.objects.filter(cart__cart_id= cart_id_(request) , product=pro)
    except Exception as e:
         raise e

    context = {
        'pro' : pro,
        'in_cart' : in_cart
    }
    return render(request, 'store_html/product-detail.html' , context   )

