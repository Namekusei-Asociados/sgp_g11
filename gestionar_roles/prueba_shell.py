from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import Group, Permission
from gestionar_roles.models import RoleSystem
from gestionar_roles.models import Permissions
from accounts.models import User
users=User.objects.all()
usuario = User.objects.get(username='romina_belen')
roles=RoleSystem.objects.all()
role=RoleSystem.objects.get(role_name='prueba1').first()
RoleSystem.objects.assing_role_to_user(role, usuario)
Role.objects.create_role(name='rolprueba29',description='porfa funciona', type_role=1, permissions_list=['gestionar_roles.list_role'])
Role.objects.list_roles_perms(8)
RoleSystem.objects.delete_role(18)
RoleSystem.objects.create_role(name='develop',description='soy una prueba',permissions_list=[2])
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
def permission_sys_required(perm, url=None, raise_exception=False):
    """Decorador para verificar si un usuario posee el permiso de sistema solicitado"""

    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if isinstance(perm, str):
                perms = (perm,)
            else:
                perms = perm

            if RoleSystem.objects.has_permissions(request.user.id, perms):
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'No tienes permisos para realizar esta accion')
                return
        return wrap

    return decorator
