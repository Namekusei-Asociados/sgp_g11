import pytest
from django.urls import reverse
from accounts.models import User
from user_story.models import UserStory
from type_us.models import TypeUS
from projects.models import ProjectMember
from projects.models import Project


@pytest.mark.django_db
def test_create_user_story(client):
    # create user
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name = 'juan', description = 'test_project')
    project_member = ProjectMember.objects.create(project=project, user=user)
    us_type = TypeUS.objects.create(prefix='test', name='name_test', flow=[('Pendiente', 'Pendiente'), ('Haciendo', 'Haciendo'), ('Finalizado', 'Finalizado')], project=project)
    assert us_type.name == 'name_test', "Error al crear Tipo de US"
    user_story = UserStory.objects.create(
        title='user_story_de_prueba',
        description='descripcion prueba',
        business_value=10,
        technical_priority=20,
        estimation_time=30,
        assigned_to=project_member,
        project_id=project.id,
        us_type_id=us_type.id
    )
    assert user_story.project_id == project.id, "Error al crear la historia de Usuario"
    assert user_story.us_type == us_type, "Error al crear la historia de Usuario"


