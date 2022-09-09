# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario de creacion del User de nuestro sistema.
    Creata registros
    """

    class Meta:
        model = User
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """
    Formulario de actualiza del User de nuestro sistema.
    Actualiza registros
    """

    class Meta:
        model = User
        fields = ("username", "email")
