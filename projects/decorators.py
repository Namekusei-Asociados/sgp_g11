from django.shortcuts import render

from accounts.models import User
from projects.models import RoleProject


def permission_proj_required(perm, url=None, raise_exception=False):
    """Decorador para verificar si un usuario posee el permiso de proyecto solicitado"""

    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if isinstance(perm, str):
                perms = (perm,)
            else:
                perms = perm

            if RoleProject.objects.has_permissions(request.user.id, kwargs['id_project'], perms):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'redirect/forbidden.html')
        return wrap

    return decorator
