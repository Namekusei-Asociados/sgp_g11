from django.core.management import call_command
from django.urls import reverse
from accounts.models import User
import pytest
from django.test import TestCase
from projects.models import PermissionsProj, RoleProject, Project, ProjectMember
from utilities.UProjectDefaultRoles import UProjectDefaultRoles


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
def test_get_index_page(client, create_logged_user):
    response = client.get(reverse('projects.index_role', kwargs={"id_project": 1}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_create_page(client, create_logged_user):
    response = client.get(reverse('projects.create_role', kwargs={"id_project": 1}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_store_role(client, create_logged_user):
    user = create_logged_user
    # create permissions
    data = {
        'name': 'Rol',
        'description': 'jeje rol',
        'perms': [1]
    }
    project = Project.objects.create(name="proj", description="descr")
    print(project.id)
    response = client.post(reverse('projects.store_role', kwargs={"id_project": project.id}), data=data,
                           follow=True)
    print(response)
    # status code success
    assert response.status_code == 200
    # role = RoleProject.objects.get(role_name='Rol')

    # check if the project was created in the database with the corrects fields
    # assert role.role_name == 'Rol'


@pytest.mark.django_db
def test_get_edit_page(client, create_logged_user):
    perms = PermissionsProj.objects.create(name='Crear_role', description="Soy un permiso")
    project = Project.objects.create(name="proj", description="descr")
    # create a role
    role = RoleProject.objects.create(role_name='Shell', description='Big project')

    # get edit form
    response = client.get(reverse('projects.edit_role', kwargs={'id': role.id, 'id_project': project.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_role(client, create_logged_user):
    project = Project.objects.create(name="proj", description="descr")
    perms1 = PermissionsProj.objects.create(name='Crear_role', description="Soy un permiso")
    # create a role
    role = RoleProject.objects.create(role_name='Shell', description='Big project')
    role.perms.add(perms1)
    role.save()
    perms2 = PermissionsProj.objects.create(name='Editar_role', description="Soy un permiso")
    role.perms.add(perms2)

    data = {
        'name': 'Shell Lubricantes',
        'description': 'Small project',
        'perms[]': [perms1.id],
        'role_id': role.id
    }

    # update project
    response = client.post(reverse('projects.update_role', kwargs={'id_project': project.id, 'id': role.id}),
                           data=data,
                           follow=True)
    assert response.status_code == 200

    # verify updated data
    # updated_role = RoleProject.objects.get(role_name='Shell Lubricantes', description='Small project')
    #
    # assert updated_role.id == role.id


@pytest.mark.django_db
def test_delete_role(client, create_logged_user):
    project = Project.objects.create(name="proj", description="descr")
    role = RoleProject.objects.create(role_name='Shell', description='Big project')
    id_role = role.id
    response = client.post(reverse('projects.delete_role', kwargs={'id_project': project.id, 'id': role.id}),
                           follow=True)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_import_role(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    roles = RoleProject.objects.create(role_name='Dev', project_id=project.id, description='Soy un dev')
    project2 = Project.objects.create(name='proyecto de Lucas', description='test_project')
    data = {
        'roles': [roles]
    }
    response = client.post(reverse('type_us.import_type_us', kwargs={"id_project": project2.id}), data=data,
                           follow=True)
    assert response.status_code == 200