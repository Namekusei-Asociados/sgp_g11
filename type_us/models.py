import json

from django.db import models

from projects.models import Project


class TypeUSManager(models.Manager):
    @staticmethod
    def create_type_us(name, prefix,flow, project_id):
        """
        Crea un registro en la base de datos con el modelo TypeUS y adjunta los custom fields

        :param name: string
        :param prefix: string
        :param flow: json

        :return: Retorna una instancia del modelo TypeUS
        """
        # create model
        type_us = TypeUS.objects.create(name=name, prefix=prefix, flow=json.dumps(flow), project_id=project_id)

        return type_us
    @staticmethod
    def update_type_us(name, prefix,flow, type_us_id):
        """
        Actualiza un registro en la base de datos con el modelo TypeUS y adjunta los custom fields

        :param name: string
        :param prefix: string
        :param flow: json

        :return: Retorna una instancia del modelo TypeUS
        """
        # create model
        type_us = TypeUS.objects.get(id=type_us_id)
        type_us.name = name
        type_us.prefix = prefix
        type_us.flow = json.dumps(flow)
        type_us.save()
        return type_us

    def get_final_status(self,id_type_us):
        type_us = TypeUS.objects.get(id=id_type_us)
        flow = json.loads(type_us.flow)
        return flow[-1]

    def get_initial_status(self, id_type_us):
        type_us = TypeUS.objects.get(id=id_type_us)
        flow = json.loads(type_us.flow)
        return flow[0]

# Create your models here.
class TypeUS(models.Model):
    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flow = models.JSONField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    objects = TypeUSManager()
