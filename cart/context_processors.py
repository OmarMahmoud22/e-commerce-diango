from .models import Cart , Cart_Item
from .utils import cart_id_




def get_quntity(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_id_(request))
            cart_item = Cart_Item.objects.all().filter(cart=cart[:1])
            for car in cart_item:
                cart_count +=car.quantity
        except Cart.DoesNotExist:
            cart_count=0        
        return dict(cart_count=cart_count)    



