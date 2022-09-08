from allauth.account.forms import PasswordField
from django import forms
from django.forms import ModelForm

from accounts.models import User


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


def username_exists(username):
    return User.objects.filter(username=username).exists()


def email_exists(email):
    return User.objects.filter(email=email).exists()


class UserForm(ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password1 = PasswordField(label="Password1", autocomplete="current-password")
    password2 = PasswordField(label="Password2", autocomplete="current-password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
