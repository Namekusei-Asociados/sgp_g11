import pytest
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from user_story.models import UserStory
from type_us.models import TypeUS
from projects.models import Project


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
def test_create_user_story(create_logged_user):
    # create user
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'),
                                          ('Finalizado', 'Finalizado')], project=project)
    assert us_type.name == 'name_test', "Error al crear Tipo de US"
    user_story = UserStory.objects.create(
        title='user_story_de_prueba',
        description='descripcion prueba',
        business_value=10,
        technical_priority=20,
        estimation_time=30,
        project_id=project.id,
        us_type_id=us_type.id
    )
    assert user_story.project_id == project.id, "Error al asignar id del proyecto a la historia de Usuario"
    assert user_story.us_type == us_type, "Error al asignar tipo de US a la historia de Usuario"


@pytest.mark.django_db
def test_cancel_user_story(create_logged_user):
    # create user
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'),
                                          ('Finalizado', 'Finalizado')], project=project)

    user_story = UserStory.objects.create(
        title='user_story_de_prueba',
        description='descripcion prueba',
        business_value=10,
        technical_priority=20,
        estimation_time=30,
        project_id=project.id,
        us_type_id=us_type.id
    )

    user_story.cancellation_reason = "por razones de testing"
    user_story.current_status = 'canceled'
    user_story.save()

    us = UserStory.objects.get(id=user_story.id)

    assert us.current_status == 'canceled', "La historia de usuario no se ha cancelado"
    assert us.cancellation_reason == 'por razones de testing', "Error al guardar motivo de cancelacion"
