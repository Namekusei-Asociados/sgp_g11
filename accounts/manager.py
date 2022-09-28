from django.contrib.auth.models import BaseUserManager

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
        user.role=RoleSystem.objects.get(role_name='Visitante')
        print(user.role)
        user.set_password(password)
        user.save()
        print(user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['role'] = 'admin'
        extra_fields['is_active'] = True
        return self.create_user(email, password, **extra_fields)
