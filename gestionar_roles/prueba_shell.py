from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import Group, Permission
from gestionar_roles.models import RoleSystem
from gestionar_roles.models import Permissions
from projects.models import RoleProject
from projects.models import PermissionsProj
from projects.models import Project
from projects.models import ProjectMember
from utilities.UProjectDefaultRoles import UProjectDefaultRoles
from accounts.models import User

scrum=UProjectDefaultRoles.get_scrum_master()
users=User.objects.all()
projects=Project.objects.all()
project=Project.objects.get(id=1)
RoleProject.objects.get_project_roles(project.id)
permiso1=PermissionsProj.objects.get(id=1)
usuario = User.objects.get(username='romina_belen')

role2=RoleProject.objects.get(id=4)
RoleProject.objects.update_user_role(usuario.id,project.id,[role2])

RoleProject.objects.create_role(name='Scrum Master',description='soy una visita',permissions_list=[])
from accounts.models import User
roles=RoleSystem.objects.all()
role=RoleSystem.objects.get(role_name='develop')
RoleSystem.objects.assing_role_to_user(role, usuario)
RoleSystem.objects.delete_role(18)
RoleSystem.objects.create_role(name='Visitante',description='soy una visita',permissions_list=[])
RoleSystem.objects.filter(user__username='romina').exists()
RoleSystem.objects.get(id=1)

RoleSystem.objects.has_permissions(2,['CRUD roles'])
RoleSystem.objects.has_permissions(3,['Configurar proyecto'])

RoleSystem.objects.edith_role(1, 'pruebaN', 'jeje', [permiso2])
RoleSystem.objects.list_role_permission(2)
def permission_sys_required(perm, url=None, raise_exception=False):
    """Decorador para verificar si un usuario posee el permiso de sistema solicitado"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            def check_perms():
                """
                Verificamos si el usuario tiene el permiso solicitado
                :param user: usuario
                :return: None
                """
                user = request.user
                if isinstance(perm, str):
                    perms = (perm,)
                else:
                    perms = perm

                retorno = RoleSystem.objects.has_permissions(user.id, perms)

                print('retorno', retorno)

                if(retorno):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.warning(request, 'No posee los permisos necesarios')
                    return render(request, "dashboard/404.html")

        return _wrapped_view
    return decorator
def permission_sys_required(perm, url=None, raise_exception=False):
    """Decorador para verificar si un usuario posee el permiso de sistema solicitado"""

    def check_perms(user):
        """
        Verificamos si el usuario tiene el permiso solicitado
        :param user: usuario
        :return: None
        """
        if isinstance(perm,str):
            perms=(perm,)
        else:
            perms=perm

        retorno= RoleSystem.objects.has_permissions(user.id, perms)
        return retorno
    return user_passes_test(check_perms, login_url=url)

