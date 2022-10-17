import os
import pytest
from django import setup
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from accounts.usecase import UserUseCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sga.settings")
setup()


@pytest.fixture
def create_logged_user(client) -> User:
    call_command('loaddata', 'permissions')
    call_command('loaddata', 'permissionsProj')
    call_command('loaddata', 'default_roles_system')
    # call_command('loaddata', 'admin')

    data = {
        'username':  'test',
    'first_name':  'first_name',
    'last_name':  'last_name',
    'email':  'email@gmail.com',
    'password':  'password',
    'role_sys':  1,
    'role_system':  1,
    }
    client.post(reverse('accounts.validate_user'),data=data, follow=True)

    user = User.objects.get(username="test")
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_is_not_user(create_logged_user):
    user = User()
    user.role_sys = ""
    assert user.role_sys != "user", "User es user"


@pytest.mark.django_db
def test_is_user(create_logged_user):
    user = User()
    user.role_sys = "user"
    user.save()
    assert user.role_sys == "user", "User no es user"


@pytest.mark.django_db
def test_is_not_admin(create_logged_user):
    user = User()
    user.role_sys = ""
    assert user.role_sys != "admin", "User es admin"


@pytest.mark.django_db
def test_is_admin(create_logged_user):
    user = User()
    user.role_sys = "admin"
    user.save()
    assert user.role_sys == "admin", "User no es admin"


@pytest.mark.django_db
def test_update_system_role(create_logged_user):
    """
    Prueba para actualizar el rol del sistema
    """
    user1 = User()
    user1.role_sys = "user"
    user1.email = "user1@gmail.com"
    user1.username = "username1"
    user1.save()
    user2 = User()
    user2.role_sys = "admin"
    user2.email = "user2@gmail.com"
    user2.username = "username2"
    user2.save()
    user1 = UserUseCase.update_system_role(user1.id, "admin")
    user2 = UserUseCase.update_system_role(user2.id, "user")
    assert user1.role_sys == "admin", "Actualización de rol fallida"
    assert user2.role_sys == "user", "Actualización de rol fallida"


@pytest.mark.django_db
def test_user_create(create_logged_user):
    user = User.objects.create_user(username='juan', email='Juan@gmaill.com', password='123')
    assert user.email == 'Juan@gmaill.com', "El usuario no se ha creado correctamente"
