from django.contrib import admin
from .models import Product , Category , Variation
# Register your models here.



class Varadmin(admin.ModelAdmin):
    list_display=('product' , 'variation_category' , 'variation_value' , 'is_active')
    list_editable = ('is_active' ,)
admin.site.register(Variation , Varadmin)
#
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price')
    prepopulated_fields = {'slug' : ('name' ,)}

admin.site.register(Product , ProductAdmin)
#
class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name' ,)}

admin.site.register(Category , CatAdmin)