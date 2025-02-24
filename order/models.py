from django.db import models
from account.models import Account
from store.models import Product , Variation
# Create your models here.

class Payment(models.Model):
    user =models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50)
    payment_method = models.CharField( max_length=50)
    amount_paid= models.CharField( max_length=50)
    status= models.CharField( max_length=50)
    created_at = models.DateTimeField(  auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):

    STATUS = (
        ('NEW', 'NEW'),
        ('ACCEPTED' , 'ACCEPTED'),
        ('COMPLETED' , 'COMPLETED'),
        ('CANCELLED','CANCELLED')

    ) 
    user =models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL , null=True , blank=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=50)
    order_totel = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50 , choices=STATUS , default='NEW')
    ip = models.CharField( max_length=50)
    is_orderd = models.BooleanField()
    created_at = models.DateTimeField(  auto_now_add=True)
    updated_at = models.DateTimeField(  auto_now=True)
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    def __str__(self):
        return self.first_name
    


class Order_Product(models.Model)    :
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user =models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    variation =models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    is_orderd = models.BooleanField(default=True)
    created_at = models.DateTimeField(  auto_now_add=True)
    updated_at = models.DateTimeField(  auto_now=True)

    
    def __str__(self):
        return self.product.name



   
    
    


