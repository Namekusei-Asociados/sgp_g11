from django.db.models import Q

from accounts.models import User


class UserUseCase:

    @staticmethod
    def update_system_role(user_id, role):
        user = User.objects.get(id=user_id)
        user.role_system = role
        user.save()
        return user

