import json

from django.db import models

from projects.models import Project


class TypeUSManager(models.Manager):
    @staticmethod
    def create_type_us(name, prefix, custom_fields_type, custom_fields_name, flow, project_id):
        """
        Crea un registro en la base de datos con el modelo TypeUS y adjunta los custom fields
        :param name: string
        :param prefix: string
        :param custom_fields_type: string
        :param custom_fields_name: string
        :param flow: json
        :return: Retorna una instancia del modelo TypeUS
        """
        # create model
        type_us = TypeUS.objects.create(name=name, prefix=prefix, flow=json.dumps(flow),project_id=project_id)

        # attach custom fields
        for i, custom_field_name in enumerate(custom_fields_name):
            custom_field= CustomFields.objects.create(name=custom_field_name, type_field=custom_fields_type[i])
            type_us.custom_fields.add(custom_field)

        return type_us


class CustomFields(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_field = models.CharField(max_length=50)
    value = models.JSONField(null=True)


# Create your models here.
class TypeUS(models.Model):
    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flow = models.JSONField()
    custom_fields = models.ManyToManyField(CustomFields)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    objects = TypeUSManager()
