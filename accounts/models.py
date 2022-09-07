from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_SYS = (
        ('user', 'user'),
        ('admin', 'admin'),
        ('visitor', 'visitor'),
    )
    role_sys = models.CharField(max_length=7, choices=ROLE_SYS, default='visitor')
    role_project = models.CharField(max_length=50, default='develop')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'''Username: {self.username}'''

