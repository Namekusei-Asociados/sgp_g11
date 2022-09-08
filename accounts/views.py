from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import User


# Create your views here.
@login_required()
def home(request):
    """
        Retorna el template home correspondiente al tipo de user logueado
        :param request: user
        :return:documento html
    """
    user = request.user
    if user.role_sys == 'visitor':
        return render(request, 'visitor.html')
    else:
        users = User.objects.all()
        users = filter(lambda x: not x.is_staff and user.username != x.username, users)
        return render(request, 'user.html', {'users': users})


def create_user(request):
    return render(request, 'create_user.html')


def edit_user(request):
    return render(request, 'edit_user.html')


def edit_user(request, username):
    user = User.objects.get(username=username)
    return render(request, 'edit_user.html', {'u': user})


def validate_edit_user(request):
    return redirect(home)


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
