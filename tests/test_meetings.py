import pytest
from django.core.management import call_command
from django.urls import reverse

from accounts.models import User
from projects.models import Project
from meetings.models import Meeting


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
def test_create_meeeting(create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    meeting = Meeting.objects.create(
        meeting_name='reunion de prueba',
        meeting_date='2021-05-05',
        meeting_details='detalles de la reunion',
        project_id=project.id
    )
    assert meeting.project_id == project.id, "Error al asignar id del proyecto a la reunion"
    assert Meeting.objects.count() == 1, "Error al crear la reunion"


@pytest.mark.django_db
def test_meeting_index(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    meeting = Meeting.objects.create(
        meeting_name='reunion de prueba',
        meeting_date='2021-05-05',
        meeting_details='detalles de la reunion',
        project_id=project.id
    )
    assert meeting.project_id == project.id, "Error al asignar id del proyecto a la reunion"
    assert Meeting.objects.count() == 1, "Error al crear la reunion"
    response = client.get(reverse('meetings.index', args=[project.id]))
    assert response.status_code == 200, "Error al cargar la pagina de reuniones"


@pytest.mark.django_db
def test_meeting_edit_view(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    meeting = Meeting.objects.create(
        meeting_name='reunion de prueba',
        meeting_date='2021-05-05',
        meeting_details='detalles de la reunion',
        project_id=project.id
    )
    assert meeting.project_id == project.id, "Error al asignar id del proyecto a la reunion"
    assert Meeting.objects.count() == 1, "Error al crear la reunion"
    response = client.get(reverse('meetings.edit', kwargs={"id_project": project.id, "id": meeting.id}))
    assert response.status_code == 200, "Error al cargar la pagina de editar reuniones"


@pytest.mark.django_db
def test_meeting_details_view(client, create_logged_user):
    project = Project.objects.create(name='proyecto de juan', description='test_project')
    assert project.name == 'proyecto de juan', 'Error al crar el proyecto'
    meeting = Meeting.objects.create(
        meeting_name='reunion de prueba',
        meeting_date='2021-05-05',
        meeting_details='detalles de la reunion',
        project_id=project.id
    )
    assert meeting.project_id == project.id, "Error al asignar id del proyecto a la reunion"
    assert Meeting.objects.count() == 1, "Error al crear la reunion"
    response = client.get(reverse('meetings.details', kwargs={"id_project": project.id, "id": meeting.id}))
    assert response.status_code == 200, "Error al cargar la pagina de detalles de reuniones"

