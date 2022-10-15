import json

from django.shortcuts import render, redirect

from projects.decorators import permission_proj_required
from projects.models import Project
from accounts.models import User
from django.contrib import messages
from django.urls import reverse

from type_us.forms import ImportTypeUs
from type_us.models import TypeUS
from utilities.UPermissionsProj import UPermissionsProject
from utilities.UProject import UProject


# Create your views here.
@permission_proj_required(UPermissionsProject.READ_TYPEUS)
def index(request, id_project):
    # get all projects related to the current user
    project = Project.objects.get(id=id_project)
    types_us = project.typeus_set.all().order_by('id')
    return render(request, 'type_us/index.html', {"types_us": types_us, "id_project": id_project})


@permission_proj_required(UPermissionsProject.CREATE_TYPEUS)
def create(request, id_project):
    """
    Retorna un formulario de creacion para Tipos de historias de usuario
    :param request:
    :return:documento html
    """
    type_custom_fields = UProject.CUSTOM_FIELDS_LIST
    columns = ['To do', 'Doing', 'Done']
    return render(request, 'type_us/create.html',{'type_custom_fields':type_custom_fields, 'id_project':id_project, 'columns':columns})


@permission_proj_required(UPermissionsProject.CREATE_TYPEUS)
def store(request, id_project):
    """
    Crea un nuevo recurso del modelo TypeUS
    :param request:
    """
    # getting attributes
    name = request.POST['name']
    prefix = request.POST['prefix']
    flow = request.POST.getlist('flow[]')

    # create type us
    type_us = TypeUS.objects.create_type_us(name=name, prefix=prefix,flow=flow, project_id=id_project)

    # redirect back with success message
    messages.success(request, 'El tipo de historia de usuario "' + type_us.name + '" fue creado exitosamente')
    return redirect(reverse('type_us.create', kwargs={'id_project': id_project}), request)


@permission_proj_required(UPermissionsProject.IMPORT_TYPEUS)
def import_type_us(request, id_project):
    """
        Importacion de roles de proyectos

        :param request: posee los campos
        :param id_project: id del proyecto actual

        :return: Documento Html
        """
    if request.method == "POST":
        types_to_import = request.POST.getlist("types")
        form = ImportTypeUs(id_project, request.POST)

        if form.is_valid():
            for type_id in types_to_import:
                typeUs = TypeUS.objects.get(id=type_id)
                new_type = TypeUS(
                    prefix=typeUs.prefix,
                    name=typeUs.name,
                    flow=typeUs.flow,
                    project_id=id_project,
                )
                new_type.save()
            messages.success(request, f'La importación fue realizada exitosamente')
            return redirect(reverse('type_us.index', kwargs={"id_project": id_project}), request)

    form = ImportTypeUs(id_project=id_project)
    current_types = TypeUS.objects.filter(project_id=id_project)
    current_types_names = [typeUs.name for typeUs in current_types]

    types_list = TypeUS.objects.exclude(name__in=current_types_names)
    context = {"form": form, "id_project": id_project, "typesUs": types_list}

    return render(request, "type_us/import_type_us.html", context)
