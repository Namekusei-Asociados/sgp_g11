import pytest


# Test the Pytest library
def test_working():
    pass


# Test the admin view
def test_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200
