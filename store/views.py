from django.shortcuts import render , get_object_or_404
from .models import Product , Category
# Create your views here.

def home(request , cat_slug=None):
    cat = None
    pro = None
    if cat_slug != None :
        cat = get_object_or_404(Category , slug = cat_slug)
        pro = Product.objects.filter(category=cat , is_available = True )
        product_count = pro.count()
    else :    
        pro = Product.objects.all().filter(is_available = True)
        product_count = pro.count()

    context = {
        'products' : pro,
        'product_count' : product_count

        }
    return render(request , 'store_html/search-result.html' , context)


def product_detail(request, cat_slug, slug_product):
    try:
        pro = get_object_or_404(Product , category__slug = cat_slug   ,slug=slug_product)
    except Exception as e:
         raise e

    context = {
        'pro' : pro
    }
    return render(request, 'store_html/product-detail.html' , context   )

