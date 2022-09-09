from django.shortcuts import render, redirect
from .models import Project
from accounts.models import User
from django.contrib import messages
from django.urls import reverse
from utilities.UProject import UProject

# Create your views here.
def index(request):
    # get all projects
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {"projects": projects})


def create(request):
    """
    Retorna un formulario de creacion para proyectos
    :param request:
    :return:documento html
    """
    users = User.objects.all()
    return render(request, 'projects/create.html', {"users": users})


def store(request):
    """
    Intenta crear un nuevo recurso del modelo Project
    :param request:
    :return:
    """
    # getting attributes
    name = request.POST['name']
    description = request.POST['description']
    user_id = request.POST['user']

    # get user
    try:
        scrum_master = User.objects.get(id=user_id)
    except:
        # redirect back with error message
        messages.success(request, 'El usuario enviado no existe')
        return redirect(reverse('projects.create'), request)

    # create project record and then attach scrum master
    project = Project.objects.create(name=name, description=description, status = UProject.STATUS_PENDING)
    project.members.add(scrum_master)

    # redirect back with success message
    messages.success(request, 'EL proyecto fue creado con exito')
    return redirect(reverse('projects.create'), request)


def edit(request, id):
    """
    Retorna la vista de edicion del projecto actual
    :param request:
    :param id: campo del modelo Project
    :return: formulario de edicion de proyecto
    """
    # get project
    project = Project.objects.get(id=id)
    users = User.objects.all()
    members = project.members.all()
    return render(request, 'projects/edit.html', {'project': project, 'users': users, 'members': members})


def update(request):
    """
    Actualiza un recurso del modelo Project
    :param request: posee los campos a modificar
    :param id: campo del modelo Project
    :return: formulario de edicion de proyecto
    """
    # get fields from edit form
    name = request.POST['name']
    description = request.POST['description']
    users = request.POST.getlist('users[]')
    project_id = request.POST['project_id']

    # get project and update
    project = Project.objects.get(id=project_id)

    # detach members
    members = project.members.values_list('id', flat=True)
    print(users)
    for member in members:
        if str(member) not in users:
            project.members.remove(str(member))

    # attach members
    project.members.add(*users)

    # update fields
    project.name = name
    project.description = description
    project.save()

    messages.success(request, 'EL proyecto fue actualizado con exito')
    return redirect(reverse('projects.edit', kwargs={'id': project.id}), request)
