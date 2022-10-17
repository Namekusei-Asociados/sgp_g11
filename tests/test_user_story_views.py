from django.core.management import call_command
from django.urls import reverse
from django.test import Client
from accounts.models import User
from projects.models import Project
import pytest


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
def test_backlog_view(create_logged_user):
    client = Client()
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='juan', description='test_project')
    response = client.get(reverse('user_story.backlog', kwargs={'id_project': project.id}))
    assert response.status_code == 200
