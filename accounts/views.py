from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
import projects.views
from accounts.models import User
from gestionar_roles.models import RoleSystem
from gestionar_roles.decorators import permission_sys_required
from utilities.UPermissions import UPermissions


# Create your views here.
@login_required()
def home(request):
    user = request.user
    if user.role.all().count() == 0:
        role_visitor = RoleSystem.objects.get(role_name='Visitante')
        RoleSystem.objects.assing_role_to_user(role_visitor, user)
    if user.role.filter(role_name='Visitante'):
        return render(request, 'accounts/visitor.html')
    return projects.views.index(request)


@permission_sys_required(UPermissions.READ_USER)
@login_required()
def index(request):
    """
       Retorna el template home correspondiente al tipo de user logueado

       :param request: user

       :return: documento html
    """
    user = request.user
    users = User.objects.all()
    users = filter(lambda x: not x.is_staff and user.username != x.username, users)
    return render(request, 'accounts/user.html', {'users': users})


@permission_sys_required(UPermissions.CREATE_USER)
def create_user(request):
    roles = RoleSystem.objects.all()
    return render(request, 'accounts/create_user.html', {'roles': roles})


@permission_sys_required(UPermissions.UPDATE_USER)
def edit_user(request, username):
    """
    Retorna una página para editar un usuario en cuestión

    :param request: user
    :param username: usuario a ser modificado

    :return: documento HTML con la información del usuario a ser actualizado
    """
    roles = RoleSystem.objects.all()
    user = User.objects.get(username=username)
    try:
        role_system = RoleSystem.objects.get(user=user)
    except RoleSystem.DoesNotExist:
        role_system = None

    return render(request, 'accounts/edit_user.html', {'u': user, 'roles': roles, 'role_system': role_system})


@permission_sys_required(UPermissions.UPDATE_USER)
def validate_edit_user(request):
    """
    Valida el usuario a ser actualizado y realiza la actualización de los datos

    :param request: formulario para edit user

    :return: HTML con los datos del usuario actualizado
    """
    username = request.POST['user_username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    roles = request.POST['role_system']

    # RoleSystem.objects.update_role_user(roles,user)

    user.save()
    user = User.objects.get(username=username)
    role = RoleSystem.objects.get(id=roles)
    RoleSystem.objects.update_role_user(role, user)
    message = 'El usuario: ' + username + ' fue actualizado con éxito'
    messages.success(request, message)
    return redirect(reverse('accounts.edit_user', kwargs={'username': user.username}), request)


@permission_sys_required(UPermissions.CREATE_USER)
def validate_user(request):
    """
        Valida que el user que se está creando cumpla las condiciones necesarias y si es así redirije al home del sitio,
        en caso contrario envia un mensaje del tipo de error

        :param request: formulario

        :return:documento html
    """
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    role_sys = request.POST['role_sys']
    id_role = request.POST['role_system']

    if username_exists(username):
        messages.success(request, 'El username ya existe')
        return redirect(reverse('accounts.create_user'), request)

    if email_exists(email):
        messages.success(request, 'El email ya existe')
        return redirect(reverse('accounts.create_user'), request)

    User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                             password=password, role_sys=role_sys)
    user = User.objects.get(username=username)
    role = RoleSystem.objects.get(id=id_role)
    RoleSystem.objects.assing_role_to_user(role, user)

    return redirect(reverse('accounts.index'), request)


def username_exists(username):
    return User.objects.filter(username=username).exists()


def email_exists(email):
    return User.objects.filter(email=email).exists()


@permission_sys_required(UPermissions.DELETE_USER)
def destroy(request, username):
    """
    Elimina un usuario

    :param request:
    :param username: usuario a ser eliminado

    :return: Documento HTML del home
    """
    user = User.objects.get(username=username)
    deleted_user_name = user.username
    user.delete()
    messages.success(request, 'El usuario' + deleted_user_name + 'fue eliminado con éxito')
    return redirect(reverse('accounts.index'), request)
