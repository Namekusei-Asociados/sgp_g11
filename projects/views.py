from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import User
from .models import Project


# Create your views here.
def create(request):
    """
    Retorna un formulario de creacion para proyectos
    :param request:
    :return:documento html
    """
    users = User.objects.all()
    users = filter(lambda x: x.role_sys != 'visitor' and not x.is_staff, users)
    return render(request, 'create.html', {"users": users})


def store(request):
    """
    Intenta crear un nuevo recurso del modelo Project
    :param request:
    :return:
    """

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
    project = Project.objects.create(name=name, description=description)
    project.members.add(scrum_master)

    # redirect back with success message
    messages.success(request, 'El proyecto fue creado con exito')
    return redirect(reverse('projects.create'), request)
