from django.urls import reverse
from accounts.models import User
import pytest
from django.test import TestCase
from projects.models import PermissionsProj, RoleProject, Project


class ProjectTest(TestCase):
    fixtures = ['default_roles_system.json', 'permissions.json', 'permissionsProj.json', 'admin.json']

    @pytest.mark.django_db
    def test_get_index_page(self):
        response = self.client.get(reverse('projects.index_role', kwargs={"id_project": 1}))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_create_page(self):
        response = self.client.get(reverse('projects.create_role', kwargs={"id_project": 1}))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_store_role(self):
        # create permissions
        perms = PermissionsProj.objects.create(name='Crear_role', description="Soy un permiso")
        data = {
            'name': 'Rol',
            'description': 'jeje rol',
            'perms': [1]
        }
        project = Project.objects.create(name="proj", description="descr")
        response = self.client.post(reverse('projects.store_role', kwargs={"id_project": project.id}), data=data,
                                    follow=True)

        # status code success
        assert response.status_code == 200
        # role = RoleProject.objects.get(role_name='Rol', description='jeje rol')
        #
        # # check if the project was created in the database with the corrects fields
        # assert role.role_name == 'Rol' and role.description == 'jeje rol'

    @pytest.mark.django_db
    def test_get_edit_page(self):
        perms = PermissionsProj.objects.create(name='Crear_role', description="Soy un permiso")
        project = Project.objects.create(name="proj", description="descr")
        # create a role
        role = RoleProject.objects.create(role_name='Shell', description='Big project')

        # get edit form
        response = self.client.get(reverse('projects.edit_role', kwargs={'id': role.id, 'id_project': project.id}))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_role(self):
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
        response = self.client.post(reverse('projects.update_role', kwargs={'id_project': project.id, 'id': role.id}),
                                    data=data,
                                    follow=True)
        assert response.status_code == 200

        # # verify updated data
        # updated_role = RoleProject.objects.get(role_name='Shell Lubricantes', description='Small project')
        #
        # assert updated_role.id == role.id

    @pytest.mark.django_db
    def test_delete_role(self):
        project = Project.objects.create(name="proj", description="descr")
        role = RoleProject.objects.create(role_name='Shell', description='Big project')
        id_role = role.id
        response = self.client.post(reverse('projects.delete_role', kwargs={'id_project': project.id, 'id': role.id}),
                                    follow=True)
        assert 200 == response.status_code
