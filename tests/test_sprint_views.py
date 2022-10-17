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
