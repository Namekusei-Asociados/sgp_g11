from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from accounts.models import User
import pytest
from django.test import TestCase
from gestionar_roles.models import Permissions, RoleSystem


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
def test_home_view(create_logged_user):
    client = Client()
    user = User.objects.create(username='test_user', password='password')
    user.save()
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_user_view(create_logged_user):
    client = Client()
    perms = Permissions.objects.get(id=2)
    rol = RoleSystem.objects.create(role_name='test')
    rol.perms.add(perms)
    user = User.objects.create(username='test_user', password='password')
    rol.user.add(user)
    response = client.get(reverse('accounts.edit_user', kwargs={'username': user.username}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_user_view(create_logged_user):
    client = Client()
    user = User.objects.create(username='test_user', password='password')
    response = client.get(reverse('accounts.delete', kwargs={'username': user.username}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_view(create_logged_user):
    client = Client()
    response = client.get(reverse('accounts.create_user'))
    assert response.status_code == 200
