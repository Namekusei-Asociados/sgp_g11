from django import template

from accounts.models import User
from projects.models import RoleProject, ProjectMember, Project
from projects.models import RoleProject, ProjectMember
from sprints.models import Sprint
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
def is_auth_user_scrum_master(user,project_id):
    member = ProjectMember.objects.get(user_id=user.id, project_id=project_id)
    return member.roles.filter(role_name=UProjectDefaultRoles.SCRUM_MASTER).exists()

@register.simple_tag
def is_member(user, id_project):
    return ProjectMember.objects.filter(user_id=user.id, project_id=id_project).exists()


@register.simple_tag
def get_project_name(id_project):
    return Project.objects.get(id=id_project).name


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


@register.simple_tag
def current_status(us_id):
    if UserStory.objects.is_initial_status(us_id):
        return 'initial'  # estado 1
    elif UserStory.objects.is_final_status(us_id):
        return 'final'  # estado final
    return 'middle'  # estado intermedio


@register.simple_tag
def can_read_burndown_chart(id_sprint):
    sprint = Sprint.objects.get(id=id_sprint)
    return sprint.status != 'pending' and not (sprint.status == 'canceled' and sprint.end_at == None)
