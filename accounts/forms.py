from allauth.account.forms import PasswordField
from django import forms
from django.forms import ModelForm

from accounts.models import User


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = PasswordField(label="Password1", autocomplete="current-password")
    password2 = PasswordField(label="Password2", autocomplete="current-password")


class UserForm(ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = PasswordField(label="Password1", autocomplete="current-password")
    password2 = PasswordField(label="Password2", autocomplete="current-password")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
