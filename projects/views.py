from django.shortcuts import render, redirect

from gestionar_roles.models import RoleSystem
from utilities.UPermissionsProj import UPermissionsProject
from utilities.UPermissions import UPermissions
from utilities.UProjectDefaultRoles import UProjectDefaultRoles
from .models import Project, RoleProject, PermissionsProj
from accounts.models import User
from django.contrib import messages
from django.urls import reverse
from .decorators import permission_proj_required
from gestionar_roles.decorators import permission_sys_required
from utilities.UProject import UProject


# Create your views here.
@permission_sys_required(UPermissions.READ_ALL_PROJECT)
def index(request):
    # get all projects related to the current user
    user = request.user
    if RoleSystem.objects.has_permissions(user.id, 'Read all project'):
        projects = Project.objects.all()
    else:
        projects = user.project_set.all()

    return render(request, 'projects/index.html', {"projects": projects})


@permission_sys_required(UPermissions.CREATE_PROJECT)
def create(request):
    """
    Retorna un formulario de creacion para proyectos

    :param request:

    :return:documento html
    """
    users = User.objects.all()
    users = filter(lambda x: not x.role.filter(role_name='Visitante').exists() and not x.is_staff, users)
    return render(request, 'projects/create.html', {"users": users})


@permission_sys_required(UPermissions.CREATE_PROJECT)
def store(request):
    """
    Intenta crear un nuevo recurso del modelo Project

    :param request:
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
    project = Project.objects.create_project(name=name, description=description, scrum_master=scrum_master)

    # redirect back with success message
    messages.success(request, 'El proyecto fue creado con exito')
    return redirect(reverse('projects.create'), request)


@permission_proj_required(UPermissionsProject.UPDATE_PROJECT)
def edit(request, id_project):
    """
    Retorna la vista de edicion del projecto actual

    :param request:
    :param id: campo del modelo Project

    :return: formulario de edicion de proyecto
    """
    # get project
    project = Project.objects.get(id=id_project)
    users = User.objects.all()
    users = filter(lambda x: not x.role.filter(role_name='Visitante').exists() and not x.is_staff, users)
    members = project.members.all()
    return render(request, 'projects/edit.html', {'project': project, 'users': users, 'members': members})


@permission_proj_required(UPermissionsProject.UPDATE_PROJECT)
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

    for member in members:
        if str(member) not in users:
            project.members.remove(str(member))

    # attach members with default role
    role = RoleProject.objects.get(project=project, role_name=UProjectDefaultRoles.DEVELOPER)

    current_members = list(project.members.values_list('id', flat=True))
    for user in users:
        if int(user) not in current_members:
            Project.objects.add_member(user, [role], project)

    # # update fields
    project.name = name
    project.description = description
    project.save()

    messages.success(request, 'El proyecto fue actualizado con exito')
    return redirect(reverse('projects.edit', kwargs={'id_project': project.id}), request)


@permission_proj_required(UPermissionsProject.CANCEL_PROJECT)
def cancel(request, id_project):
    """
    Intenta cancelar un proyecto

    :param request:
    :param project_id: id del registro proyecto

    :return: documento html
    """
    project = Project.objects.get(id=id_project)
    return render(request, 'projects/cancel.html', {'project': project, 'id_project': id_project})


@permission_proj_required(UPermissionsProject.CANCEL_PROJECT)
def validate_cancel_project(request, id_project):
    cancellation_reason = request.POST['cancellation_reason']

    # get project and update
    project = Project.objects.get(id=id_project)
    project.cancellation_reason = cancellation_reason
    project.status = UProject.STATUS_CANCELED
    project.save()
    messages.success(request, 'El proyecto "' + project.name + '" fue cancelado con éxito')
    return redirect(reverse('projects.index'), request)


def dashboard(request, id_project):
    return render(request, 'projects/base/app.html', {'id_project': id_project})


@permission_proj_required(UPermissionsProject.READ_PROJECTMEMBER)
def members(request, id_project):
    """
    Muestra la lista de miembros de un proyecto

    :param request:
    :param id_project: id del proyecto actual

    :return: documento html
    """
    members = Project.objects.get_project_members(id_project)
    print(members)
    return render(request, 'projects/members/index.html', {"members": members, 'id_project': id_project})


@permission_proj_required(UPermissionsProject.CREATE_PROJECTMEMBER)
def create_member(request, id_project):
    """
    Crea un miembro del proyecto

    :param request:
    :param id_project: id del proyecto actual

    :return: documento html
    """
    project = Project.objects.get(id=id_project)
    roles = project.roleproject_set.all()

    # get all users that has not been attached to this project
    current_members = project.members.all()
    all_users = User.objects.all()

    users = list(set(all_users) - set(current_members))
    print(users)
    return render(request, 'projects/members/create.html', {"roles": roles, 'id_project': id_project, 'users': users})


@permission_proj_required(UPermissionsProject.UPDATE_PROJECTMEMBER)
def edit_member(request, id_project, member_id):
    """
    Muestra los datos para la edicion de un miembro

    :param request:
    :param id_project: id del proyecto
    :param member_id: id del miembro a editar

    :return: Documento HTML
    """
    project = Project.objects.get(id=id_project)
    roles = project.roleproject_set.all()

    member = User.objects.get(id=member_id)
    current_roles = RoleProject.objects.get_member_roles(id_user=member_id, id_project=id_project)
    return render(request, 'projects/members/edit.html',
                  {"roles": roles, "current_roles": current_roles, 'id_project': id_project, 'member': member})


@permission_proj_required(UPermissionsProject.UPDATE_PROJECTMEMBER)
def update_member(request, id_project, member_id):
    roles_id = request.POST.getlist('roles[]')

    # attach new members to the project
    project = Project.objects.get(id=id_project)
    roles = [RoleProject.objects.get(id=item) for item in roles_id]
    RoleProject.objects.update_user_role(id_user=member_id, id_project=id_project, roles=roles)

    messages.success(request, 'El miembro se actualizo con exito')
    return redirect(reverse('projects.members.edit', kwargs={'id_project': project.id, 'member_id': member_id}),
                    request)


@permission_proj_required(UPermissionsProject.CREATE_PROJECTMEMBER)
def store_member(request, id_project):
    """
    Agrega un nuevo miembro al proyecto actual

    :param request:
    :param id_project:

    :return: Documento html
    """
    user_id = request.POST['user_id']
    roles = request.POST.getlist('roles[]')

    # attach new members to the project
    project = Project.objects.get(id=id_project)
    Project.objects.add_member(user_id=user_id, roles=roles, project=project)

    messages.success(request, 'El miembro se agrego al proyecto con exito')
    return redirect(reverse('projects.members.create', kwargs={'id_project': project.id}), request)


###########ROLES#############
@permission_proj_required(UPermissionsProject.CREATE_ROLE)
def create_role(request, id_project):
    """
    Retorna un formulario de creacion de roles

    :param id_project:  id del proyecto
    :param request:

    :return: documento html
    """
    permission = PermissionsProj.objects.all()
    return render(request, 'roles/create.html', {"permissions": permission, "id_project": id_project})


@permission_proj_required(UPermissionsProject.CREATE_ROLE)
def store_role(request, id_project):
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

    RoleProject.objects.create_role(name=name, description=description, permissions_list=perms, id_project=id_project)

    messages.success(request, 'El rol "' + name + '" fue creado exitosamente')
    return redirect(reverse('projects.create_role', kwargs={"id_project": id_project}), request)


@permission_proj_required(UPermissionsProject.READ_ROLE)
def index_role(request, id_project):
    """
    Muestra la lista de usuarios de un proyecto

    :param request:
    :param id_project: id del proyecto

    :return: Documento HTML
    """
    # get all Roles
    roles = RoleProject.objects.get_project_roles(id_project)

    return render(request, 'roles/index.html', {"roles": roles, "id_project": id_project})


@permission_proj_required(UPermissionsProject.UPDATE_ROLE)
def edit_role(request, id_project, id):
    """
    Retorna la vista de edicion del rol actual

    :param request:
    :param id: campo del modelo rol
    :param id_project: id del proyecto actual

    :return: formulario de edicion de rol
    """
    # get project
    role = RoleProject.objects.get(id=id)
    permissions = PermissionsProj.objects.all()
    perms_role = role.perms.all()
    return render(request, 'roles/edit.html',
                  {'role': role, 'permissions': permissions, 'perms_role': perms_role, "id_project": id_project,
                   'id': id})


@permission_proj_required(UPermissionsProject.UPDATE_ROLE)
def update_role(request, id_project, id):
    """
        Actualiza un recurso del modelo rol

        :param id_project: id del proyecto actual
        :param request: posee los campos a modificar

        :return: formulario de edicion de rol
        """
    # get fields from edit form
    name = request.POST['name']
    description = request.POST['description']
    perms = request.POST.getlist('perms[]')
    role_id = request.POST['role_id']
    permissions = [PermissionsProj.objects.get(id=item) for item in perms]
    # permissions=Permissions.objects.get(id__in=perms)
    # print(permissions)
    role = RoleProject.objects.get(id=role_id)
    # get project and update
    RoleProject.objects.update_role(id_role=role_id, name=name, description=description, perms=permissions)

    messages.success(request, 'El rol "' + name + '" fue actualizado exitosamente')

    return redirect(reverse('projects.edit_role', kwargs={'id': role.id, "id_project": id_project}), request)


@permission_proj_required(UPermissionsProject.DELETE_ROLE)
def delete_role(request, id_project, id):
    """
    Elimina un recurso del modelo roles

    :param request: posee los campos a modificar
    :param id: campo del modelo roles

    :return: formulario de eliminacion de rol
    """
    role = RoleProject.objects.get(id=id)
    RoleProject.objects.delete_role(id)
    messages.success(request, 'El rol fue eliminado con éxito')
    return redirect(reverse('projects.index_role', kwargs={"id_project": id_project}), request)
