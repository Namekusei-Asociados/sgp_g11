from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from gestionar_roles.decorators import permission_sys_required
from gestionar_roles.models import RoleSystem, Permissions
from utilities.UPermissions import UPermissions


@permission_sys_required(UPermissions.CREATE_ROLE)
# Create your views here.
def create(request):
    """
    Retorna un formulario de creacion de roles

    :param request:
    :return: documento html
    """
    permission = Permissions.objects.all()
    return render(request, 'gestionar_roles/create.html', {"permissions": permission})


@permission_sys_required(UPermissions.CREATE_ROLE)
def store(request):
    """
    Funcion para guardar los un rol

    :param request: request post
    :return:
    """
    name = request.POST['name']
    description = request.POST['description']
    perms = request.POST.getlist('perms[]')
    print(name, description, perms)
    print(perms)

    result=RoleSystem.objects.create_role(name, description, perms)
    if result:
        messages.success(request, 'El rol "' + name + '" fue creado exitosamente')
    else:
        messages.error(request, f'Ya existe un rol llamado "{name}"')
    return redirect(reverse('gestionar_roles.create'), request)


@permission_sys_required(UPermissions.READ_ROLE)
def index(request):
    # get all Roles
    roles = RoleSystem.objects.all()

    return render(request, 'gestionar_roles/index.html', {"roles": roles})


@permission_sys_required(UPermissions.UPDATE_ROLE)
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


@permission_sys_required(UPermissions.UPDATE_ROLE)
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
    permissions = [Permissions.objects.get(id=item) for item in perms]
    # permissions=Permissions.objects.get(id__in=perms)
    # print(permissions)
    role = RoleSystem.objects.get(id=role_id)
    # get project and update
    RoleSystem.objects.update_role(id_role=role_id, name=name, description=description, perms=permissions)

    messages.success(request, 'El rol "' + name + '" fue actualizado exitosamente')
    return redirect(reverse('gestionar_roles.edit', kwargs={'id': role.id}), request)


@permission_sys_required(UPermissions.DELETE_ROLE)
def delete(request, id):
    """
    Elimina un recurso del modelo roles

    :param request: posee los campos a modificar
    :param id: campo del modelo roles

    :return: formulario de eliminacion de rol
    """
    role = RoleSystem.objects.get(id=id)

    result=RoleSystem.objects.delete_role(id)
    if result:
        messages.success(request, f'El rol "{role.role_name}" fue eliminado con éxito')
    else:
        messages.error(request, f'El rol "{role.role_name}" posee miembros y no puede ser eliminado')
    return redirect(reverse('gestionar_roles.index'), request)
