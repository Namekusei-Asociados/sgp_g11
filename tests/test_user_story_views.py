from django.core.management import call_command
from django.urls import reverse
from django.test import Client
from accounts.models import User
from projects.models import Project
import pytest

from type_us.models import TypeUS
from user_story.models import UserStory


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


@pytest.mark.django_db
def test_index_page_history(client, create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=['Pendiente', 'Haciendo', 'Finalizado'], project=project)

    user_story = UserStory.objects.create(
        title='user_story_de_prueba',
        description='descripcion prueba',
        business_value=10,
        technical_priority=20,
        estimation_time=30,
        project_id=project.id,
        us_type_id=us_type.id
    )

    response = client.get(
        reverse('user_story.history', kwargs={"id_project": project.id, 'id_user_story': user_story.id}))
    assert response.status_code == 200
