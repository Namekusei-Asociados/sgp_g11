from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import User


# Create your views here.
@login_required()
def home(request):
    """
        Retorna el template home correspondiente al tipo de user logueado
        :param request: user
        :return: documento html
    """
    user = request.user
    if user.role_sys == 'visitor':
        return render(request, 'accounts/visitor.html')
    else:
        users = User.objects.all()
        users = filter(lambda x: not x.is_staff and user.username != x.username, users)
        return render(request, 'accounts/user.html', {'users': users})


def create_user(request):
    return render(request, 'accounts/create_user.html')


def edit_user(request, username):
    """
    Retorna una página para editar un usuario en cuestión
    :param request: user
    :param username: usuario a ser modificado
    :return: documento HTML con la información del usuario a ser actualizado
    """
    user = User.objects.get(username=username)
    return render(request, 'accounts/edit_user.html', {'u': user})


def validate_edit_user(request):
    """
    Valida el usuario a ser actualizado y realiza la actualización de los datos

    :param request: formulario para edit user

    :return: HTML con los datos del usuario actualizado
    """
    username = request.POST['user_username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    role_sys = request.POST['role_sys']
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.role_sys = role_sys
    user.save()
    messages.success(request, 'El usuario fue actualizado con éxito')
    return redirect(reverse('accounts.edit_user', kwargs={'username': user.username}), request)


def validate_user(request):
    """
    Valida que el user que se está creando cumpla las condiciones necesarias y si es así redirije al home del sitio,
    en caso contrario envia un mensaje del tipo de error

    :param request: formulario

    :return: documento html
    """
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    role_sys = request.POST['role_sys']

    if username_exists(username):
        messages.success(request, 'El username ya existe')
        return redirect(reverse('accounts.create_user'), request)

    if email_exists(email):
        messages.success(request, 'El email ya existe')
        return redirect(reverse('accounts.create_user'), request)

    User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                             password=password, role_sys=role_sys)

    return redirect(home)


def username_exists(username):
    return User.objects.filter(username=username).exists()


def email_exists(email):
    return User.objects.filter(email=email).exists()


def destroy(request, username):
    """
    Elimina un usuario
    :param request:
    :param username: usuario a ser eliminado
    :return: Documento HTML del home
    """
    user = User.objects.get(username=username)
    user.delete()
    messages.success(request, 'El usuario fue eliminado con éxito')
    return redirect(reverse('home'), request)
