from urllib.parse import urlparse, parse_qs
from django.http.response import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode 
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#
from django.contrib.auth.decorators import login_required
from django.contrib import messages ,auth
from .models import Account,MyAccountManager
from django.shortcuts import render , redirect , get_object_or_404
from .form import RegesterForm 
from cart.models import Cart,Cart_Item
from cart.utils import cart_id_
# Create your views here.
def regester(request):
    if request.method =='POST':
        form = RegesterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name , last_name=last_name , email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()


            current_site= get_current_site(request)
            mail_subject = 'please actuvate your account'
            message = render_to_string('account/account_verification_email.html',{
                 'user':user,
                 'domain':current_site,
                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                 #تشفير ال يوزر ايدي لانه يرسل للسمتخدم
                 'token':default_token_generator.make_token(user)

            })
            to_email=email
            send_email =EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()

            #messages.success(request,'susccess')
            return redirect('/account/login/?command=verification&email='+email)
        
    else:
            form = RegesterForm()    
            messages.error(request,'error')
    context = {
                'form':form

            }

    return render(request,'account/register.html' , context)


def activate(request , uidb64 , token):
     try:
          uid= urlsafe_base64_decode(uidb64).decode()
          #لكي يتم البحث عن ال يوزر ايدي يجب فك الترميز اولا
          user = Account._default_manager.get(pk=uid)
     except(TypeError,ValueError,OverflowError , Account.DoesNotExist)     :
          user = None

     if user is not None and default_token_generator.check_token(user , token):
              user.is_active=True
              user.save()
              messages.success(request,'sucsses activeated')
              return redirect('login')
     else:
            messages.error(request,'error')
            return redirect('regester')
         

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                # استرجاع السلة
                cart_id = cart_id_(request)
                # التحقق من وجود السلة أو إنشائها إذا لم تكن موجودة
                cart = Cart.objects.get(cart_id=cart_id)
                # التحقق من وجود عناصر داخل السلة
                is_cart_item_exist = Cart_Item.objects.filter(cart=cart , is_active=True).exists()
                if is_cart_item_exist:
                    # تحديث المستخدم لعناصر السلة
                    cart_item=Cart_Item.objects.filter(cart=cart)
                    product_varitation=[]
                    for item in cart_item:
                         varitation = item.varitations.all()
                         product_varitation.append(list(varitation))


                    cart_item = Cart_Item.objects.filter(user=user)
                    ex_vat_list = []
                    id = []
                    for item in cart_item:
                         existing_varitation = item.varitations.all()  # استرجاع المتغيرات (الخيارات) الخاصة بكل عنصر في السلة
                         ex_vat_list.append(list(existing_varitation))  # إضافة قائمة المتغيرات للعناصر الموجودة في سلة المستخدم
                         id.append(item.id)  # تخزين معرف العنصر في قائمة id
                         for pr in product_varitation:  # التكرار على المنتجات في السلة المؤقتة
                              if pr in ex_vat_list:  # إذا كانت المتغيرات نفسها موجودة في قائمة المستخدم
                                  index = ex_vat_list.index(pr)  # الحصول على موقع المنتج في القائمة
                                  item_id = id[index]  # استخراج معرف المنتج باستخدام نفس الموقع
                                  item = Cart_Item.objects.get(id=item_id)
                                  item.quantity += 1
                                  item.user = user # تحديث المستخدم للعنصر
                                  item.save()
                    else:
                         cart_item = Cart_Item.objects.filter(cart=cart)
                         for item in cart_item:
                              item.user=user 
                              item.save()

            except Exception as e:
                print(f"Error in cart item handling: {e}")
            
            auth.login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح.')
            url = request.META.get('HTTP_REFERER', '')

            try:
                query = urlparse(url).query  # next=/profile/&user=omar استخراج الجزء الخاص بالـ query من الرابط
                params = parse_qs(query)     # {'next': ['/profile/'], 'user': ['omar']} تحليل الـ query وتحويله إلى قاموس
            
                if 'next' in params:
                    next_page = params['next'][0]  # استخراج القيمة الأولى من القائمة
                    return redirect(next_page)
            
            except:
                    return redirect('dashboard')

            
        else:
            messages.error(request, 'خطأ في البريد الإلكتروني أو كلمة المرور.')
            return redirect('login')

    return render(request, 'account/signin.html')


@login_required(login_url='login')
def logout(request):
     auth.logout(request)
     messages.success(request,'logged out')
     return redirect('login')







def forget_password(request)         :
     if request.method == 'POST':
          email = request.POST['email']
          if Account.objects.filter(email=email).exists():
               user = Account.objects.get(email__exact=email)

               currebt_site = get_current_site(request)
               message_subject = "please rest your password"
               message = render_to_string('account/reset_password_validation.html',{
                    'user':user,
                    'domain':currebt_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user)

               })
               to_email = email
               send_email = EmailMessage(message_subject ,message ,to=[to_email])
               send_email.send()
               messages.success(request , 'sucsses')
               return redirect('login')
          else:
               messages.error(request , 'error')
               return redirect('forget')
          


     return render(request,'account/forget_password.html')



def rest_password_validatoin(request,uidb64 , token):
     try:
          uid = urlsafe_base64_decode(uidb64).decode()
          user = Account._default_manager.get(pk=uid)
     except(TypeError , ValueError ,Account.DoesNotExist)     :
          user=None
     if user is not None and default_token_generator.check_token(user,token)     :
          request.session['uid']=uid
          messages.success(request,'sucsses')
          return redirect('rest_password')
     else:
          messages.error(request,'error')
          return redirect('login')

     
     
def rest_password(request)     :
     if request.method == 'POST':

          password = request.POST['password']
          confirm_password = request.POST['confirm_password']
          if password == confirm_password:
               uid=request.session.get('uid')
               user = Account.objects.get(pk=uid)
               user.set_password(password)
               user.save()
               messages.success(request,'sucsses')
               return redirect('login')
          else:
               messages.error(request,'error')
               return redirect('rest_password')

     else:

          return render(request , 'account/rest_password.html')


def dashboard(request):
     return render(request , 'account/dashboard.html')


