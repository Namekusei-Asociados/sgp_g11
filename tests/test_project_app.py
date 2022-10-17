import pytest
from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from gestionar_roles.models import RoleSystem
from projects.models import Project, PermissionsProj
from utilities.UPermissionsProj import UPermissionsProject
from django.core.management import call_command

# class ProjectTest(TestCase):






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


# @pytest.mark.django_db
# def test_get_index_page(client , create_logged_user):
#
#     # ProjectTest()
#     print('****************')
#
#     print(create_logged_user)
#
#     print('****************')
#
#     response = client.get(reverse('projects.index'))
#
#     assert response.status_code == 200
    # @pytest.fixture
    # def project_with_(db) ->User:
    #     user =

    # @pytest.mark.django_db
    # def test_get_create_page(client):
    #     response = client.get(reverse('projects.create'))
    #     assert response.status_code == 200

@pytest.mark.django_db
def test_store_project(client, create_logged_user):
    # create user
    user = create_logged_user

    data = {
        'name': 'juan',
        'description': 'Huge project',
        'user':user.id
    }
    response = client.post(reverse('projects.store'), data=data, follow=True)

    # status code success
    assert response.status_code == 200
    print("***********************************")
    print(response)
    print(Project.objects.all().count())
    print("***********************************")
    project = Project.objects.get(name='juan', description='Huge project')

    # check if the project was created in the database with the corrects fields
    assert project.name == 'juan' and project.description == 'Huge project'
    #
    # @pytest.mark.django_db
    # def test_get_edit_page(client, create_permissions):
    #     # create user
    #     user = User.objects.create(username='test_user', password='password')
    #     user.save()
    #     # create a project
    #     project = Project.objects.create(name='Shell', description='Big project')
    #     project.save()
    #
    #     # get edit form
    #     response = client.get(reverse('projects.edit', kwargs={'id': project.id}))
    #     assert response.status_code == 200
    #
    # # @pytest.mark.django_db
    # # def test_update_project(client, create_permissions):
    # #     # create users
    # #     user = User.objects.create(username='test_user_1', password='password')
    # #     user.save()
    # #
    # #     second_user = User.objects.create(username='test_user_2', password='password')
    # #     second_user.save()
    # #
    # #     # create a project
    # #     project = Project.objects.create(name='Shell', description='Big project')
    # #
    # #     Project.objects.add_member(user_id=user.id, roles=[],project=project)
    # #     project.save()
    # #
    # #     data = {
    # #         'name': 'Shell Lubricantes',
    # #         'description': 'Small project',
    # #         'users[]': [second_user.id],
    # #         'project_id': project.id
    # #     }
    # #
    # #     # update project
    # #     response = client.post(reverse('projects.update'), data=data, follow=True)
    # #     assert response.status_code == 200
    # #
    # #     # verify updated data
    # #     updated_project = Project.objects.get(name='Shell Lubricantes', description='Small project',members=second_user)
    # #
    # #     assert updated_project.id == project.id
