from django import template
from projects.models import RoleProject, ProjectMember
from type_us.models import TypeUS
from user_story.models import UserStory
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
def can_edit_type_us(type_us_id):
    """
    Comprueba si el tipo de us actual puede o no ser editado

    :param type_us_id: id de type us

    :return: boolean
    """
    return not UserStory.objects.filter(us_type=type_us_id).exists()

@register.simple_tag
def can_delete_type_us(type_us_id):
    """
    Comprueba si el tipo de us actual puede o no ser eliminado

    :param type_us_id: id de type us

    :return: boolean
    """
    return not UserStory.objects.filter(us_type=type_us_id).exists()