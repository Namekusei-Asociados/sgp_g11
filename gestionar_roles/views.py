from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from gestionar_roles.models import RoleSystem, Permissions


# Create your views here.
def create(request):
    """
    Retorna un formulario de creacion de roles

    :param request:
    :return: documento html
    """
    permission = Permissions.objects.all()
    return render(request, 'gestionar_roles/create.html', {"permissions": permission})


def store(request):
    name = request.POST['name']
    description = request.POST['description']
    perms = request.POST.getlist('perms[]')
    print(name, description, perms)
    print(perms)

    RoleSystem.objects.create_role(name, description, perms)

    messages.success(request, 'El rol fue creado con exito')
    return redirect(reverse('gestionar_roles.create'), request)


def index(request):
    # get all Roles
    roles = RoleSystem.objects.all()

    return render(request, 'gestionar_roles/index.html', {"roles": roles})


def edit(request, id):
    """
    Retorna la vista de edicion del rol actual

    :param request:
    :param id: campo del modelo rol

    :return: formulario de edicion de rol
    """
    # get project
    role = RoleSystem.objects.get(id=id)
    permissions = Permissions.objects.all()
    perms_role = role.perms.all()
    return render(request, 'gestionar_roles/edit.html',
                  {'role': role, 'permissions': permissions, 'perms_role': perms_role})


def update(request):
    """
        Actualiza un recurso del modelo rol

        :param request: posee los campos a modificar
        :param id: campo del modelo rol

        :return: formulario de edicion de rol
        """
    # get fields from edit form
    name = request.POST['name']
    description = request.POST['description']
    perms = request.POST.getlist('perms[]')
    role_id = request.POST['role_id']
    permissions=[Permissions.objects.get(id=item) for item in perms]
    #permissions=Permissions.objects.get(id__in=perms)
    #print(permissions)
    role = RoleSystem.objects.get(id=role_id)
    # get project and update
    RoleSystem.objects.update_role(id_role=role_id, name=name, description=description, perms=permissions)

    return redirect(reverse('gestionar_roles.edit', kwargs={'id': role.id}), request)
