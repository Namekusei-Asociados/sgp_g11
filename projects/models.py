from django.conf import settings
from django.db import models
from accounts.models import User
from gestionar_roles.models import Permissions
class RoleProjectManager(models.Manager):
    pass
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True)
    members = models.ManyToManyField(User)
    status = models.CharField(max_length=50)
    # def __str__(self) -> str:
    #     text = "{0}"
    #     return text.format(self.name)

class RoleProject(models.Model):
    """
    Roles de sistema
    """
    # campos de los roles en la base de datos
    role_name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)
    # asociamos los roles a permisos
    perms = models.ManyToManyField(Permissions)

    objects = RoleProjectManager()

    def __str__(self):
        return f'{self.role_name}'

