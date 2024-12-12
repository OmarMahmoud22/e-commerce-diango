from django.urls import path
from . import views

app_name='cart'
urlpatterns=[
    path('' , views.cart , name='cart_details'),
    path('add_cart/<int:product_id>' , views.add_cart ,name='add_cart'),
    path('remove_item/<int:product_id>' , views.remove_cart_item , name = "remove_item"),
    path('remove_cart/<int:product_id>' , views.mainus , name = "mainus"),

]