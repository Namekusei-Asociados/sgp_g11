from django.test import TestCase
from django.test import Client
from django.urls import reverse
from accounts.models import User
import pytest

from gestionar_roles.models import Permissions, RoleSystem


class ProjectTest(TestCase):
    fixtures = ['default_roles_system.json', 'permissions.json', 'permissionsProj.json', 'admin.json']

    @pytest.mark.django_db
    def test_verifyPermissions(self):
        role = RoleSystem.objects.get(id=1)
        self.assertEqual(role.role_name, "Admin")

    def test_get_index_page(self):
        client = Client()
        response = client.get(reverse('gestionar_roles.index'))
        assert response.status_code == 200

    def test_get_create_page(self):
        client = Client()
        response = client.get(reverse('gestionar_roles.create'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_store_role(self):
        client = Client()
        # create permissions
        data = {
            'name': 'Rol',
            'description': 'jeje rol',
            'perms': [1]
        }
        response = client.post(reverse('gestionar_roles.store'), data=data, follow=True)

        # status code success
        assert response.status_code == 200
        # role = RoleSystem.objects.get(role_name='Rol', description='jeje rol')
        #
        # # check if the project was created in the database with the corrects fields
        # assert role.role_name == 'Rol' and role.description == 'jeje rol'

    @pytest.mark.django_db
    def test_get_edit_page(self):
        client = Client()
        # create a role
        role = RoleSystem.objects.create(role_name='Shell', description='Big project')

        # get edit form
        response = client.get(reverse('gestionar_roles.edit', kwargs={'id': role.id}))
        assert response.status_code == 200

    #
    @pytest.mark.django_db
    def test_update_role(self):
        client = Client()
        perms1 = Permissions.objects.get(name='Create role')
        # create a project
        role = RoleSystem.objects.create(role_name='Shell', description='Big project')
        role.perms.add(perms1)
        role.save()

        data = {
            'name': 'Shell Lubricantes',
            'description': 'Small project',
            'perms': [perms1],
            'id_role': role.id
        }
        print(RoleSystem.objects.all())
        response = self.client.get(reverse('gestionar_roles.update'), data=data)
        # prueba=RoleSystem.objects.update_role(**data)
        # updated=RoleSystem.objects.get(role_name='Shell Lubricantes')
        # update project
        self.assertEqual(200, response.status_code, RoleSystem.objects.all())

        @pytest.mark.django_db
        def test_delete_role(client):
            role = RoleSystem.objects.create(role_name='Shell', description='Big project')
            id_role = role.id
            response = client.post(reverse('gestionar_roles.delete', kwargs={'id': role.id}),
                                   follow=True)
            assert 200 == response.status_code
