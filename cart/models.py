from django.db import models
from store.models import Product,Variation
from account.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , unique=True)
    date_added = models.DateField( auto_now_add=True)


    def __str__(Self):
        return Self.cart_id
    

class Cart_Item(models.Model):
    user = models.ForeignKey(Account,  on_delete=models.CASCADE , null=True)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    varitations = models.ManyToManyField(Variation , blank=True)
    cart  = models.ForeignKey(Cart,  on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
     
    def __str__(self) :
        return str(self.product)
    
    def suptotal(slef):
        return slef.product.price * slef.quantity
        

    
