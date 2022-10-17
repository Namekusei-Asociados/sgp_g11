from django.core.management import call_command
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from accounts.models import User
import pytest

from gestionar_roles.models import Permissions, RoleSystem


@pytest.fixture
def create_logged_user(client) -> User:
    call_command('loaddata', 'permissions')
    call_command('loaddata', 'permissionsProj')
    call_command('loaddata', 'default_roles_system')
    # call_command('loaddata', 'admin')

    data = {
        'username': 'test',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@gmail.com',
        'password': 'password',
        'role_sys': 1,
        'role_system': 1,
    }
    client.post(reverse('accounts.validate_user'), data=data, follow=True)

    user = User.objects.get(username="test")
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_verifyPermissions(client, create_logged_user):
    role = RoleSystem.objects.get(id=1)
    assert role.role_name == "Admin"


@pytest.mark.django_db
def test_get_index_page(client, create_logged_user):
    response = client.get(reverse('gestionar_roles.index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_create_page(client, create_logged_user):
    response = client.get(reverse('gestionar_roles.create'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_store_role(client, create_logged_user):
    # create permissions
    data = {
        'name': 'Rol',
        'description': 'jeje rol',
        'perms': [1]
    }
    response = client.post(reverse('gestionar_roles.store'), data=data, follow=True)

    # status code success
    assert response.status_code == 200
    role = RoleSystem.objects.get(role_name='Rol', description='jeje rol')
    #
    # # check if the project was created in the database with the corrects fields
    assert role.role_name == 'Rol' and role.description == 'jeje rol'


@pytest.mark.django_db
def test_get_edit_page(client, create_logged_user):
    # create a role
    role = RoleSystem.objects.create(role_name='Shell', description='Big project')

    # get edit form
    response = client.get(reverse('gestionar_roles.edit', kwargs={'id': role.id}))
    assert response.status_code == 200


#
@pytest.mark.django_db
def test_update_role(client, create_logged_user):
    perms1 = Permissions.objects.get(name='Create role')
    # create a project
    role = RoleSystem(role_name='Dev', description='Soy un developer')
    role.save()
    role.perms.add(perms1)

    data = {
        'name': 'Shell Lubricantes',
        'description': 'Small project',
        'perms': [perms1],
        'role_id': role.id
    }
    print(RoleSystem.objects.all())
    response = client.post(reverse('gestionar_roles.update'), data=data, follow=True)
    assert response.status_code == 200

    updated = RoleSystem.objects.get(role_name='Shell Lubricantes')
    # update project
    assert updated.id == role.id


@pytest.mark.django_db
def test_delete_role(client, create_logged_user):
    role = RoleSystem.objects.create(role_name='Shell', description='Big project')
    id_role = role.id
