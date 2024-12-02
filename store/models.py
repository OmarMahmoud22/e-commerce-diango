from django.db import models
from django.urls import reverse
# Create your models here.






class Category(models.Model):
    name = models.CharField( max_length=50)
    slug = models.SlugField(max_length=50 , unique=True)
    description = models.TextField()
    cat_image = models.ImageField( upload_to='photo/cate',blank=True , null=True)

    def get_absolute_url(self):
        return reverse("product_by_cat", args=[self.slug])
    

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField( max_length=50 , unique=True)
    slug = models.SlugField( max_length=50 , unique=True)
    description = models.TextField()
    price = models.DecimalField( max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product/images')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=False)
    modified_date = models.DateTimeField(auto_now=False)

    def get_url(self):
        return reverse('detais_product', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

   










