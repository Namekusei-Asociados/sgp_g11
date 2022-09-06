from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True)
    members = models.ManyToManyField(User)
    # def __str__(self) -> str:
    #     text = "{0}"
    #     return text.format(self.name)
