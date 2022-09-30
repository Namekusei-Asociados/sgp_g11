import pytest
from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from gestionar_roles.models import RoleSystem
from projects.models import Project, PermissionsProj
from utilities.UPermissionsProj import UPermissionsProject


# @pytest.mark.usefixtures("create_user")
# class ProjectTest(TestCase):
#
#     fixtures = ['default_roles_system.json', 'permissions.json', 'permissionsProj.json', 'admin.json']
#
#
#     def test_get_index_page(self):
#         print('****************')
#         print(self.create_user)
#         print('****************')
#         response = self.client.get(reverse('projects.index'))
#         assert response.status_code == 500
#
# @pytest.fixture(scope="class")
# def create_user(db) -> RoleSystem:
#     return User.objects.get(id=1)

    # @pytest.fixture
    # def project_with_(db) ->User:
    #     user =

    # @pytest.mark.django_db
    # def test_get_create_page(client):
    #     response = client.get(reverse('projects.create'))
    #     assert response.status_code == 200

    # @pytest.mark.django_db
    # def test_store_project(client, create_permissions):
    #     # create user
    #     user = User.objects.create(username='test_user', password='password')
    #     user.save()
    #
    #     data = {
    #         'name': 'juan',
    #         'description': 'Huge project',
    #         'user': user.id
    #     }
    #     response = client.post(reverse('projects.store'), data=data, follow=True)
    #
    #     # status code success
    #     assert response.status_code == 200
    #     project = Project.objects.get(name='juan', description='Huge project')
    #
    #     # check if the project was created in the database with the corrects fields
    #     assert project.name == 'juan' and project.description == 'Huge project'
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
