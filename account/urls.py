from django.urls import path
from . import views


urlpatterns = [
    path('login/' , views.login, name = 'login'),
    path('regester/' , views.regester , name = 'regester'),
    path('logout/' , views.logout , name='logout'),
    path('activate/<uidb64>/<token>', views.activate , name='acivate'),
    path('forget_password/',views.forget_password , name='forget'),
    path('rest_password_validatoin/<uidb64>/<token>' , views.rest_password_validatoin , name='rest_password_validatoin'),
    path('rest_password/',views.rest_password , name='rest_password'),
    path('dashboard/' , views.dashboard , name='dashboard'),
    


    
    

]
