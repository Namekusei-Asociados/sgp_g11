from django.shortcuts import render, redirect
from projects.models import Project
from accounts.models import User
from django.contrib import messages
from django.urls import reverse
from utilities.UProject import UProject

# Create your views here.
def index(request):
    # get all projects related to the current user
    user = request.user

    projects = user.project_set.all()
    return render(request, 'projects/index.html', {"projects": projects})


def create(request):
    """
    Retorna un formulario de creacion para proyectos
    :param request:
    :return:documento html
    """
    users = User.objects.all()
    users = filter(lambda x: x.role_sys != 'visitor' and not x.is_staff, users)
    return render(request, 'type_us/create.html', {"users": users})
