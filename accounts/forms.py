from allauth.account.forms import PasswordField
from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = PasswordField(label="Password1", autocomplete="current-password")
    password2 = PasswordField(label="Password2", autocomplete="current-password")
