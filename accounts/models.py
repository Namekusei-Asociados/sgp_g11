from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
    Este modulo tiene el modelo de user personalizado de nuestro sistema
    Para manejo de roles y campos de formularios
"""
from gestionar_roles.models import RoleSystem


class CustomUserManager(BaseUserManager):
    """
    Hereda BaseUserManager de Django para el manejo del modelo del User del sistema
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        print(user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['role'] = 'admin'
        extra_fields['is_active'] = True
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    El User hereda el AbstractUser de DJango.
    Se personaliza atributos
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = CustomUserManager()

    def __str__(self):
        return f'''Username: {self.username} | Email: {self.email}'''


@receiver(post_save, sender=User)
def assing_iniciate_rol(sender, instance, **kwargs):
    role_admin = RoleSystem.objects.get(role_name='Admin')
    role_visitor = RoleSystem.objects.get(role_name='Visitante')
    if User.objects.all().count() == 1:
        instance.role.add(role_admin)
    elif instance.role.all().count() == 0:
        instance.role.add(role_visitor)
