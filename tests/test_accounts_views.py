from django.test import Client
from django.urls import reverse
from accounts.models import User
import pytest
from django.test import TestCase
from gestionar_roles.models import Permissions, RoleSystem


class TestAccountViews(TestCase):
    fixtures = ['default_roles_system.json', 'permissions.json', 'permissionsProj.json', 'admin.json']

    @pytest.mark.django_db
    def test_home_view(self):
        client = Client()
        user = User.objects.create(username='test_user', password='password')
        user.save()
        client.force_login(user)
        response = client.get(reverse('home'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_edit_user_view(self):
        client = Client()
        perms = Permissions.objects.get(id=2)
        rol = RoleSystem.objects.create(role_name='test')
        rol.perms.add(perms)
        user = User.objects.create(username='test_user', password='password')
        rol.user.add(user)
        response = client.get(reverse('accounts.edit_user', kwargs={'username': user.username}))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_user_view(self):
        client = Client()
        user = User.objects.create(username='test_user', password='password')
        response = client.get(reverse('accounts.delete', kwargs={'username': user.username}))
        assert response.status_code == 200

    def test_create_user_view(self):
        client = Client()
        response = client.get(reverse('accounts.create_user'))
        assert response.status_code == 200
