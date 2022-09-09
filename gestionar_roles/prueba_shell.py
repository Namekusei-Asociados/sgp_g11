from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import Group, Permission
from gestionar_roles.models import Role
from accounts.models import User
users=User.objects.all()
user=users[2]
Role.objects.create_role(name='rolprueba29',description='porfa funciona', type_role=1, permissions_list=['gestionar_roles.list_role'])
Role.objects.list_roles_perms(8)
Role.objects.delete_role(18)
