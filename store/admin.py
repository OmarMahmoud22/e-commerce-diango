from django.contrib import admin
from .models import Product , Category
# Register your models here.





#
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price')
    prepopulated_fields = {'slug' : ('name' ,)}

admin.site.register(Product , ProductAdmin)
#
class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name' ,)}

admin.site.register(Category , CatAdmin)