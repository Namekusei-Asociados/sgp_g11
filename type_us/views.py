import json

from django.shortcuts import render, redirect
from projects.models import Project
from accounts.models import User
from django.contrib import messages
from django.urls import reverse

from type_us.models import TypeUS
from utilities.UProject import UProject


# Create your views here.
def index(request):
    # get all projects related to the current user
    user = request.user

    projects = user.project_set.all()
    return render(request, 'projects/index.html', {"projects": projects})


def create(request):
    """
    Retorna un formulario de creacion para Tipos de historias de usuario
    :param request:
    :return:documento html
    """
    type_custom_fields = UProject.CUSTOM_FIELDS_LIST
    return render(request, 'type_us/create.html',{'type_custom_fields':type_custom_fields})


def store(request):
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
    type_us = TypeUS.objects.create_type_us(name=name, prefix=prefix,custom_fields_type=custom_fields_type, custom_fields_name=custom_fields_name,flow=flow)

    # redirect back with success message
    messages.success(request, 'El tipo de historia de usuario se creo con exito')
    return redirect(reverse('type_us.create'), request)
