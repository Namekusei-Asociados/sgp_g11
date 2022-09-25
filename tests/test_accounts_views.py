from django.urls import reverse
from accounts.models import User
import pytest


@pytest.mark.django_db
def test_home_view(client):
    user = User.objects.create(username='test_user', password='password')
    user.save()
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_user_view(client):
    user = User.objects.create(username='test_user', password='password')
    response = client.get(reverse('accounts.edit_user', kwargs={'username': user.username}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_user_view(client):
    user = User.objects.create(username='test_user', password='password')
    response = client.get(reverse('accounts.delete', kwargs={'username': user.username}))
    assert response.status_code == 302


def test_create_user_view(client):
    response = client.get(reverse('accounts.create_user'))
    assert response.status_code == 200
