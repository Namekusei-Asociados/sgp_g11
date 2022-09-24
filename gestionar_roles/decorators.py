from django.shortcuts import render

from accounts.models import User
from gestionar_roles.models import RoleSystem


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
                return render(request, 'redirect/forbidden.html')
        return wrap

    return decorator
