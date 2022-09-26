import json

from django.shortcuts import render, redirect
from projects.models import Project
from accounts.models import User
from django.contrib import messages
from django.urls import reverse

from type_us.models import TypeUS
from utilities.UProject import UProject


# Create your views here.
def index(request,id_project):
    # get all projects related to the current user
    project = Project.objects.get(id=id_project)
    types_us = project.typeus_set.all()
    return render(request, 'type_us/index.html', {"types_us": types_us,"id_project":id_project})


def create(request,id_project):
    """
    Retorna un formulario de creacion para Tipos de historias de usuario
    :param request:
    :return:documento html
    """
    type_custom_fields = UProject.CUSTOM_FIELDS_LIST
    return render(request, 'type_us/create.html',{'type_custom_fields':type_custom_fields, 'id_project':id_project})


def store(request,id_project):
    """
    Crea un nuevo recurso del modelo TypeUS
    :param request:
    """
    # getting attributes
    name = request.POST['name']
    prefix = request.POST['prefix']
    custom_fields_name = request.POST.getlist('custom_fields[name]')
    custom_fields_type = request.POST.getlist('custom_fields[type]')
    flow = request.POST.getlist('flow[]')

    # create type us
    type_us = TypeUS.objects.create_type_us(name=name, prefix=prefix,custom_fields_type=custom_fields_type, custom_fields_name=custom_fields_name,flow=flow, project_id = id_project)

    # redirect back with success message
    messages.success(request, 'El tipo de historia de usuario se creo con exito')
    return redirect(reverse('type_us.create', kwargs={'id_project':id_project}), request)
