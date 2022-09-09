from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from gestionar_roles.models import Role


# Create your views here.
def create(request):
    """
    Retorna un formulario de creacion de roles
    :param request:
    :return: documento html
    """
    permission = Permission.objects.filter(content_type__app_label__in=['gestionar_roles', 'projects', 'accounts'])
    return render(request, 'gestionar_roles/create.html', {"permissions": permission})


def store(request):
    name = request.POST['name']
    description = request.POST['description']
    perms = request.POST.getlist('perms[]')
    print(name, description, perms)

    permissions = Permission.objects.filter(codename__in= perms)
    #for perm in perms:
     #   perms_format.append(str(perm.content_type))
    rol_nuevo = Role.objects.create_role(name,description,1,permissions)
    #print(rol_nuevo)
    messages.success(request, 'El rol fue creado con exito')
    print(request.POST)
    for permission in permissions:
        print(permission.content_type)
    #print(permissions.content_types)
    return redirect(reverse('gestionar_roles.create'), request)
