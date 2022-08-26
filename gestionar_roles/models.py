from django.contrib.auth.models import Group
from django.db import models

# Create your models here.
class Rol(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=40, null=True)
    description = models.CharField(max_length=250, null=True)
    role_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str([self.name])

