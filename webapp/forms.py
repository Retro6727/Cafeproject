from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer

class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    labels = {
        'username':'Enter username',
        'first_name':'Enter first name',
        'last_name': 'Enter last name',
        'email':'Enter email',
        'password1':'Enter password',
        'password2':'Enter confirmpassword',
    }
    widgets = { 
        'first_name': forms.TextInput(attrs={'class':'form-label'}),
        'last_name': forms.TextInput(attrs={'class':'form-label'}),
        'email': forms.TextInput(attrs={'class':'form-label'}),
        'username': forms.TextInput(attrs={'class':'form-label'}),
        'password1': forms.TextInput(attrs={'class':'form-label'}),
        'password2': forms.TextInput(attrs={'class':'form-label'}),
    }

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Enter Username",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Enter Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    class Meta:
        model=User
        fileds=['username']
'''
from .models import Food

class foodform(forms.ModelForm):
    class Meta:
        model = Food
'''

class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address' ,'city', 'state', 'pincode']
    
    labels = {
        'Name' : 'Enter your name',
        'Address' : 'Enter address',
        'City' : 'Enter city',
        'State' : 'Enter state',
        'Pincode' : 'Enter pincode',
    }

