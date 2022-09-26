from django.shortcuts import render, redirect

from utilities.UProjectDefaultRoles import UProjectDefaultRoles
from .models import Project, RoleProject, PermissionsProj
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
    return render(request, 'projects/create.html', {"users": users})


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
    return redirect(reverse('projects.edit', kwargs={'id': project.id}), request)


def dashboard(request, id_project):
    return render(request, 'projects/base/app.html', {'id_project': id_project})


def members(request, id_project):
    members = Project.objects.get_project_members(id_project)
    print(members)
    return render(request, 'projects/members.html', {"members": members,'id_project':id_project})


###########ROLES#############
def create_role(request, id_project):
    """
    Retorna un formulario de creacion de roles

    :param id_project:  id del proyecto
    :param request:

    :return: documento html
    """
    permission = PermissionsProj.objects.all()
    return render(request, 'roles/create.html', {"permissions": permission, "id_project": id_project})


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

    messages.success(request, 'El rol fue creado con exito')
    return redirect(reverse('projects.create_role', kwargs={"id_project": id_project}), request)


def index_role(request, id_project):
    # get all Roles
    roles = RoleProject.objects.get_project_roles(id_project)

    return render(request, 'roles/index.html', {"roles": roles, "id_project": id_project})


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
    messages.success(request, 'El rol fue actualizado con éxito')

    return redirect(reverse('projects.edit_role', kwargs={'id': role.id, "id_project": id_project}), request)


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
