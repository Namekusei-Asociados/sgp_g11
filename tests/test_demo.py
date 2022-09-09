import pytest

# Test the Pytest library
def test_working():
    pass


# pytestmark = pytest.mark.django_db
@pytest.mark.django_db
def test_user_create():
    assert 'usuario_prueba' == 'usuario_prueba'
