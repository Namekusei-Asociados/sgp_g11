import os

import pytest
from django import setup
from django.test import TestCase

from accounts.models import User
from accounts.usecase import UserUseCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sga.settings")
setup()


@pytest.mark.django_db
def test_user_create():
    user1 = User.objects.create_user('usuario_prueba', 'Juan@gmaill.com', '123')
    assert user1.username == 'usuario_prueba'


class TestUser(TestCase):
    """
    Clase para probar el modelo de usuario
    """

    @pytest.fixture(scope="session")
    def test_is_not_user(self):
        user = User()
        user.role_system = ""
        self.assertNotEqual(user.is_user(), True, "User es user")

    def test_is_user(self):
        user = User()
        user.role_system = "user"
        self.assertEqual(user.is_user(), True, "User no es user")

    def test_is_not_admin(self):
        user = User()
        user.role_system = ""
        self.assertNotEqual(user.is_admin(), True, "User es admin")

    def test_is_admin(self):
        user = User()
        user.role_system = "admin"
        self.assertEqual(user.is_admin(), True, "User no es admin")

    def test_update_system_role(self):
        '''
        Prueba para actualizar el rol del sistema
        '''
        user1 = User()
        user1.role_system = "user"
        user1.email = "user1@gmail.com"
        user1.save()
        user2 = User()
        user2.role_system = "admin"
        user2.email = "user2@gmail.com"
        user2.save()
        user1 = UserUseCase.update_system_role(user1.id, "admin")
        user2 = UserUseCase.update_system_role(user2.id, "user")
        self.assertEqual(user1.role_system, "admin", "Actualización de rol fallida")
        self.assertEqual(user2.role_system, "user", "Actualización de rol fallida")
