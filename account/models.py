from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    #normal users
    def create_user(self , username , email , first_name , last_name , password = None):
        if not email:
            return ValueError('user must have email')
        
        if not username:
            return ValueError('user must have username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password) #hashing
        user.save(using=self._db)
        return user
    

    def create_superuser(self , username , email , first_name , last_name , password = None):
        #admin users and useing the same function with some perms
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.suberadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField( max_length=50)
    username = models.CharField( max_length=50)
    email = models.EmailField( max_length=254 , unique=True)
    phone_number = models.CharField( max_length=50)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
#بشكل افتراضي، يقوم Django بتعيين مدير أساسي (models.Manager)،
#  لكن عند تعريف مدير مخصص مثل MyAccountManager، فإنك تستبدل السلوك الافتراضي بإضافة منطقك الخاص.

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']


    def __str__(self):
        return self.email
    
    def has_perm(self , perm , obj=None):
        return self.is_admin
    
    def has_module_perms(self , add_label):
        return True

