from django import template
from projects.models import RoleProject, ProjectMember, Project
from utilities.UProjectDefaultRoles import UProjectDefaultRoles

register = template.Library()


@register.simple_tag
def has_perm_project(user, id_project, perms):
    """Decorador para verificar si un usuario posee el permiso de proyecto solicitado"""
    return RoleProject.objects.has_permissions(user.id, id_project, perms)


@register.simple_tag
def is_scrum_master(member):
    return member.roles.filter(role_name=UProjectDefaultRoles.SCRUM_MASTER).exists()


@register.simple_tag
def is_member(user, id_project):
    return ProjectMember.objects.filter(user_id=user.id, project_id=id_project).exists()


@register.simple_tag
def get_project_name(id_project):
    return Project.objects.get(id=id_project).name
