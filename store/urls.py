from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('<slug:cat_slug>/' , views.home , name='product_by_cat') , 
    path('<slug:cat_slug>/<slug:slug_product>/' , views.product_detail , name ='detais_product' )
]
