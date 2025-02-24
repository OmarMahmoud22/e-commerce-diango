from django import forms
from .models import Account


class RegesterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password','class':'form-control'}))

    conferm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'repeate password','class':'form-control'}))
    class Meta:
        model = Account
        fields = ['first_name' , 'last_name' , 'phone_number' , 'password' , 'email']

        
    def clean(self):
         clean_data = super(RegesterForm , self).clean()
         password = clean_data.get('password')
         conferm_password = clean_data.get('conferm_password')
         if password != conferm_password:
              raise forms.ValidationError("password didnt match")


    def __init__(self , *args , **kwrgs)    :
    
            super(RegesterForm , self).__init__(*args , **kwrgs)
            self.fields['email'].widget.attrs['placeholder'] = 'enter email'
            self.fields['first_name'].widget.attrs['placeholder'] = 'enter first_name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'enter last_name'
            self.fields['phone_number'].widget.attrs['placeholder'] = 'enter phone_number'
            
            
            for item in self.fields:
                self.fields[item].widget.attrs['class'] = 'form-control'
