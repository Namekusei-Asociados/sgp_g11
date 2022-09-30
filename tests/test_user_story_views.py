from django.urls import reverse
from accounts.models import User
from projects.models import Project
import pytest


@pytest.mark.django_db
def test_backlog_view(client):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    project = Project.objects.create(name='juan', description='test_project')
    response = client.get(reverse('user_story.backlog', kwargs={'id_project': project.id}))
    assert response.status_code == 200

