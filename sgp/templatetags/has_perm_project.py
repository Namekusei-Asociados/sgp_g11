from django import template
from projects.models import RoleProject

register = template.Library()


@register.simple_tag
def has_perm_system(user, id_project, perms):
    """Decorador para verificar si un usuario posee el permiso de proyecto solicitado"""
    return RoleProject.objects.has_permissions(user.id, id_project, perms)
