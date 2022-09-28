from django.urls import reverse
from accounts.models import User
import pytest

from gestionar_roles.models import Permissions, RoleSystem


@pytest.mark.django_db
def test_get_index_page(client):
    response = client.get(reverse('gestionar_roles.index'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_create_page(client):
    response = client.get(reverse('gestionar_roles.create'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_store_role(client):
    # create permissions
    perms = Permissions.objects.create(name='Crear_role', description="Soy un permiso")
    data = {
        'name': 'Rol',
        'description': 'jeje rol',
        'perms': [1]
    }
    response = client.post(reverse('gestionar_roles.store'), data=data, follow=True)

    # status code success
    assert response.status_code == 200
    role = RoleSystem.objects.get(role_name='Rol', description='jeje rol')

    # check if the project was created in the database with the corrects fields
    assert role.role_name == 'Rol' and role.description == 'jeje rol'


@pytest.mark.django_db
def test_get_edit_page(client):
    # create a role
    role = RoleSystem.objects.create(role_name='Shell',description='Big project')

    # get edit form
    response = client.get(reverse('gestionar_roles.edit', kwargs={'id': role.id}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_role(client):
    perms1 = Permissions.objects.create(name='Crear_role', description="Soy un permiso")
    # create a project
    role = RoleSystem.objects.create(role_name='Shell', description='Big project')
    role.perms.add(perms1)
    role.save()
    perms2 = Permissions.objects.create(name='Editar_role', description="Soy un permiso")
    role.perms.add(perms2)

    data = {
        'name': 'Shell Lubricantes',
        'description': 'Small project',
        'perms[]': [perms1.id],
        'role_id': role.id
    }

    # update project
    response = client.post(reverse('gestionar_roles.update'), data=data, follow=True)
    assert response.status_code == 200

    # verify updated data
    updated_role = RoleSystem.objects.get(role_name='Shell Lubricantes', description='Small project')

    assert updated_role.id == role.id

@pytest.mark.django_db
def test_delete_role(client):
    role = RoleSystem.objects.create(role_name='Shell', description='Big project')
    id_role=role.id
    response = client.post(reverse('gestionar_roles.delete', kwargs={'id': role.id}),
                           follow=True)
    assert 0==RoleSystem.objects.filter(id=id_role).count()