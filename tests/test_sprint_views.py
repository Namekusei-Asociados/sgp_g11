import json
from _datetime import datetime
import pandas as pd
import pytest
from django.core.management import call_command
from django.shortcuts import render
from django.urls import reverse

import sprints.views
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
        'username': 'test',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@gmail.com',
        'password': 'password',
        'role_sys': 1,
        'role_system': 1,
    }
    client.post(reverse('accounts.validate_user'), data=data, follow=True)

    user = User.objects.get(username="test")
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_sprint_members_view(client, create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    sprint = Sprint.objects.create(sprint_name='Sprint Test',
                                   start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
                                   duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                                           end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
                                   number=1,
                                   project_id=project.id)

    assert sprint.sprint_name == 'Sprint Test', "No se ha creado correctamente el sprint"

    context = {
        'id_project': project.id,
        'id_sprint': sprint.id,
    }

    response = client.get(reverse('sprints.members.index', kwargs=context))

    assert response.status_code == 200


# def kanban_index(request, id_project, id_sprint):
@pytest.mark.django_db
def test_sprint_kanban_index(client, create_logged_user):
    project = Project.objects.create_project(name='proyecto de juan', description='test_project',scrum_master=create_logged_user)
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    sprint = Sprint.objects.create(sprint_name='Sprint Test',
                                   start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
                                   duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                                           end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
                                   number=1,
                                   project_id=project.id)

    assert sprint.sprint_name == 'Sprint Test', "No se ha creado correctamente el sprint"

    context = {
        'id_project': project.id,
        'id_sprint': sprint.id,
    }

    response = client.get(reverse('sprints.kanban.index', kwargs=context))
    assert response.status_code == 200


@pytest.mark.django_db
def test_sprint_kanban_user_story_change_status(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')

    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=json.dumps(['Pendiente', 'Haciendo', 'Finalizado']), project=project)

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
    data = {
        'change_to_status': 'next',
        'user_story_id': user_story.id
    }

    # update project
    response = client.post(reverse('sprints.kanban.user_story.change_status_kanban',
                                   kwargs={'id_project': project.id, 'id_sprint': sprint.id}),
                           data=data,
                           follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_sprint_kanban_task_store(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')

    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    us_type = TypeUS.objects.create(prefix='test', name='name_test',
                                    flow=json.dumps(['Pendiente', 'Haciendo', 'Finalizado']), project=project)

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
    data = {
        'description': 'Small project',
        'total_hours': 9,
        'id_user_story': user_story.id
    }

    # update project
    response = client.post(
        reverse('sprints.kanban.user_story.task_store', kwargs={'id_project': project.id, 'id_sprint': sprint.id}),
        data=data,
        follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_sprint_index(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    sprint = Sprint.objects.create(sprint_name='Sprint Test',
                                   start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                   end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
                                   duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
                                                           end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
                                   number=1,
                                   project_id=project.id)

    assert sprint.sprint_name == 'Sprint Test', "No se ha creado correctamente el sprint"

    context = {
        'id_project': project.id,
    }

    response = client.get(reverse('sprints.index', kwargs=context))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_change_member(client, create_logged_user):
#     user = User.objects.create(username='test_user', password='password')
#     user.save()
#     project = Project.objects.create(name='proyecto de juan', description='test_project')
#     assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
#
#     sprint = Sprint.objects.create(
#         sprint_name='Sprint Test',
#         start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
#         end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
#         duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
#                                 end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
#         number=1,
#         project_id=project.id
#     )
#
#     member = SprintMember.objects.create(sprint_id=sprint.id, user_id=user.id, workload=8)
#     member.save()
#
#     miembro = SprintMember.objects.get(id=member.id)
#
#     # update project
#     response = client.get(reverse('sprints.members.change', kwargs={'id_project': project.id,
#                                                                     'id_sprint': sprint.id, 'member_id': member.id}),
#                           follow=True)
#     assert response.status_code == 200


@pytest.mark.django_db
def test_validate_member(client, create_logged_user):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    user2 = User.objects.create(username='test_user2', password='password')
    user2.save()
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
    data = {
        'user_id': user.id,
        'member_to_remove': member.id,
    }
    # update project
    response = client.post(reverse('sprints.members.validate.change', kwargs={'id_project': project.id,
                                                                              'id_sprint': sprint.id}), data=data,
                           follow=True)
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_burndown_chart(client, create_logged_user):
#     project = Project.objects.create(name='proyecto de juan', description='test_project')
#
#     assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
#     us_type = TypeUS.objects.create(prefix='test', name='name_test',
#                                     flow=json.dumps(['Pendiente', 'Haciendo', 'Finalizado']), project=project)
#
#     user_story = UserStory.objects.create(
#         title='user_story_de_prueba',
#         description='descripcion prueba',
#         business_value=10,
#         technical_priority=20,
#         estimation_time=30,
#         project_id=project.id,
#         us_type_id=us_type.id
#     )
#     sprint = Sprint.objects.create(sprint_name='Sprint Test',
#                                    start_at=datetime.strptime('2022/09/30', '%Y/%m/%d'),
#                                    end_at=datetime.strptime('2022/10/15', '%Y/%m/%d'),
#                                    duration=pd.bdate_range(start=datetime.strptime('2022/09/30', '%Y/%m/%d'),
#                                                            end=datetime.strptime('2022/10/15', '%Y/%m/%d')).size,
#                                    number=1,
#                                    project_id=project.id)
#
#     assert sprint.sprint_name == 'Sprint Test', "No se ha creado correctamente el sprint"
#
#     # update project
#     response = client.get(reverse('sprints.burndown_chart',
#                                    kwargs={'id_project': project.id, 'id_sprint': sprint.id}),
#                            follow=True)
#     assert response.status_code == 200