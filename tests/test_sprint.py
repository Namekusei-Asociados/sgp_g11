from _datetime import datetime
import pandas as pd
import pytest
from django.core.management import call_command
from django.urls import reverse
from accounts.models import User
from user_story.models import UserStory
from type_us.models import TypeUS
from projects.models import Project
from sprints.models import Sprint, SprintMember


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
def test_create_sprint(create_logged_user):
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
    sprint = Sprint.objects.create(sprint_name='Sprint Test',
                                   start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
                                   duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                                           end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
                                   number=1,
                                   project_id=project.id)

    assert sprint.sprint_name == 'Sprint Test', "No se ha creado correctamente el sprint"

    user_story.sprint_id = sprint.id
    user_story.save()

    assert user_story.sprint.id == sprint.id, "No se han asociado correctamente el sprint y la US"


@pytest.mark.django_db
def test_update_sprint(create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'

    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'),
                                          ('Finalizado', 'Finalizado')], project=project)
    assert us_type.name == 'name_test', "Error al crear Tipo de US"

    sprint = Sprint.objects.create(
        sprint_name='Sprint Test',
        start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
        end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
        duration=pd.bdate_range(
            start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
            end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
        number=1,
        project_id=project.id
    )
    sprint.save()

    sprint.sprint_name = "Sprint Test 2"
    sprint.description = "Descripcion"
    sprint.duration = 10
    sprint.save()

    assert sprint.sprint_name == "Sprint Test 2", "Error al actualizar nombre de sprint"
    assert sprint.description == "Descripcion", "Error al actualizar Descripcion de sprint"
    assert sprint.duration == 10, "Error al actualizar duración de sprint"


@pytest.mark.django_db
def test_cancel_sprint(create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'

    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'),
                                          ('Finalizado', 'Finalizado')], project=project)

    sprint = Sprint.objects.create(
        sprint_name='Sprint Test',
        start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
        end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
        duration=pd.bdate_range(
            start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
            end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
        number=1,
        project_id=project.id
    )
    sprint.save()

    spr = Sprint.objects.get(id=sprint.id)

    spr.cancellation_reason = "por razones de testing"
    spr.status = 'Cancelado'
    spr.save()

    assert spr.status == 'Cancelado', "El sprint no se ha cancelado"
    assert spr.cancellation_reason == 'por razones de testing', "Error al guardar motivo de cancelacion de sprint"


@pytest.mark.django_db
def test_add_sprint_member(create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'

    sprint = Sprint.objects.create(
            sprint_name='Sprint Test',
            start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
            end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
            duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
            number=1,
            project_id=project.id
    )

    member = SprintMember.objects.create(sprint_id=sprint.id, user_id=user.id, workload=8)
    member.save()

    miembro = SprintMember.objects.get(id=member.id)

    assert miembro.workload == 8, "El miembro de sprint no se ha agregado correctamente"


@pytest.mark.django_db
def test_assign_user_story(create_logged_user):
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

    sprint = Sprint.objects.create(
            sprint_name='Sprint Test',
            start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
            end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
            duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
            number=1,
            project_id=project.id
    )

    member = SprintMember.objects.create(sprint_id=sprint.id, user_id=user.id, workload=8)

    user_story.assigned_to = member
    user_story.sprint_id = sprint.id
    user_story.save()

    us = UserStory.objects.get(id=user_story.id)

    assert us.assigned_to.user.username == 'test_user', "No se ha podido asignar el encargado a la historia de usuario"


