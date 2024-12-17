from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

