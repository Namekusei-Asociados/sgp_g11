from django import template
from gestionar_roles.models import RoleSystem

register = template.Library()


@register.simple_tag
def has_perm_system(user, perms):
    """Decorador para verificar si un usuario posee el permiso de sistema solicitado"""
    if isinstance(perms, str):
        perm = (perms,)
    else:
        perm = perms
    return RoleSystem.objects.has_permissions(user.id, perm)
