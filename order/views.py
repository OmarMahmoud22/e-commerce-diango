import datetime
from django.shortcuts import render , redirect
from cart.models import Cart_Item
from .form import OrderForm
from .models import Order
from django.http import HttpResponse
# Create your views here.


def payment(request):
        return render(request , 'store/payment.html')    




def place_order(request , total=0 , quantity=0):
    current_user =request.user

    cart_item = Cart_Item.objects.filter(user = current_user)
    cart_count = cart_item.count()
    if cart_count <0:
        return redirect('home')
    
    grand_total =0
    tax =0
    for item in cart_item:
        total += (item.quantity * item.product.price)
        quantity += item.quantity
    tax = (2*total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user 
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_totel = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.is_orderd= False
            data.save()

            today = datetime.date.today()  # ✅ استدعاء التاريخ مرة واحدة فقط
            current_date = today.strftime('%Y%m%d')  # ✅ تحويل التاريخ إلى تنسيق YYYYMMDD تحويل التاريخ الي نص 
            order_number = f"{current_date}{data.id}"  # ✅ دمج التاريخ مع ID الطلب
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user , is_orderd =False ,order_number=order_number)
            context = {
                'order':order,
                'cart_item' : cart_item,
                'grand_total' : grand_total,
                'tax':tax,
                'total':total
            }
            return render(request , 'store/payment.html' ,context)
        else:
             return HttpResponse('none')
    else:
        return redirect('cart:check_out')  
