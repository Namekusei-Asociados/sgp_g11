from django.db import models

class CustomFields(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_field = models.CharField(max_length=50)
    value = models.JSONField()


# Create your models here.
class TypeUS(models.Model):
    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flow = models.JSONField()
    custom_fields = models.ManyToManyField(CustomFields)
