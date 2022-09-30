from django.urls import reverse
from accounts.models import User
import pytest

from gestionar_roles.models import Permissions, RoleSystem


@pytest.fixture
def create_permissions(db):
    # create permissions
    Permissions.objects.create(name='test_rol', description='test')
    Permissions.objects.create(name='Test_rol', description='test')


@pytest.mark.django_db
def test_home_view(client):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_user_view(client, create_permissions):
    perms = Permissions.objects.get(id=2)
    rol = RoleSystem.objects.create(role_name='test')
    rol.perms.add(perms)
    user = User.objects.create(username='test_user', password='password')
    rol.user.add(user)
    response = client.get(reverse('accounts.edit_user', kwargs={'username': user.username}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_user_view(client):
    user = User.objects.create(username='test_user', password='password')
    response = client.get(reverse('accounts.delete', kwargs={'username': user.username}))
    assert response.status_code == 302


def test_create_user_view(client, create_permissions):
    response = client.get(reverse('accounts.create_user'))
    assert response.status_code == 200
