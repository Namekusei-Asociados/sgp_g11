from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from projects.decorators import permission_proj_required
from projects.models import Project
from user_story.models import UserStory
from utilities.UPermissionsProj import UPermissionsProject
from .models import Sprint, SprintMember


# Create your views here.

@permission_proj_required(UPermissionsProject.READ_SPRINT)
def index(request, id_project):
    """
    Devuelve la lista de sprints del proyecto

    :param id_project: id del proyecto actual
    :param request

    :return: documento HTML
    """
    sprints = Sprint.objects.filter(project_id=id_project).order_by('id')
    existsPlanning = False

    for sprint in sprints:
        if sprint.status == 'Planificacion':
            existsPlanning = True

    context = {
        'sprints': sprints,
        'id_project': id_project,
        'existsPlanning': existsPlanning
    }

    return render(request, 'sprint/index.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINT)
def create_sprint(request, id_project):
    """
    Devuelve el template para crear un nuevo sprint

    :param request
    :param id_project: id del proyecto en el cual se debe crear el sprint

    :return: documento HTML
    """

    context = {
        'id_project': id_project
    }

    return render(request, 'sprint/create_sprint.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINT)
def validate_create_sprint(request, id_project):
    """
    Función para guardar un nuevo sprint

    :param request:
    :param id_project: id del proyecto en el cual se crea el sprint

    :return: template para crear un nuevo sprint
    """
    sprint_name = request.POST['sprint_name']
    description = request.POST['description']
    duration = request.POST['duration']

    Sprint.objects.create(sprint_name=sprint_name, duration=duration, description=description,
                          number=numbersSprint(id_project), project_id=id_project)

    message = 'El sprint "' + sprint_name + '" fue creada con éxito'
    messages.success(request, message)

    return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


def daterange(start_date, end_date):
    """
    Calcula los días hábiles para un sprint

    :param start_date: fecha estimada de inicio del sprint
    :param end_date: fecha estimada de finalización del sprint

    :return: cantidad de días hábiles entre fecha de inicio y fecha de finalización del sprint
    """
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))


def numbersSprint(id_project):
    """
    Calcula el número del sprint a ser creado

    :param id_project: id del proyecto en el cual se creará el sprint

    :return: número del sprint a ser creado
    """
    return Sprint.objects.filter(project_id=id_project).count() + 1


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT)
def edit_sprint(request, id_project, id_sprint):
    """
    Retorna el template para editar un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint a ser editado

    :return: template para editar los detalles de un sprint
    """
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_project': id_project,
        'sprint': sprint
    }

    return render(request, 'sprint/edit_sprint.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT)
def validate_edit_sprint(request, id_project):
    """
    Actualiza los datos que se están editando de un sprint

    :param request:
    :param id_project: id del proyecto actual, al que pertenece el sprint que se está editando

    :return: documento HTML con la lista de sprints, con el sprint editado ya actualizado
    """
    id_sprint = request.POST['id_sprint']
    name = request.POST['sprint_name']
    description = request.POST['description']
    duration = request.POST['duration']

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.sprint_name = name
    sprint.description = description
    sprint.duration = duration

    sprint.save()

    return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


@permission_proj_required(UPermissionsProject.DELETE_SPRINT)
def cancel_sprint(request, id_project, id_sprint):
    """
    Devuelve un template solicitando el motivo de la cancelación del sprint

    :param request
    :param id_project: id del proyecto al que pertenece el sprint a ser cancelado
    :param id_sprint: id del sprint a ser cancelado

    :return: template para ingresar el motivo de la cancelación del sprint
    """
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_project': id_project,
        'sprint': sprint
    }

    return render(request, 'sprint/cancel_sprint.html', context)


@permission_proj_required(UPermissionsProject.DELETE_SPRINT)
def validate_cancel_sprint(request, id_project):
    """
    Guarda el motivo de la cancelación de un sprint y realiza la
    actualización de su estado a "Cancelado"

    :param request
    :param id_project: id del proyecto actual, al que pertenece el sprint a ser cancelado

    :return: documento HTML de la lista de sprints del proyecto actual
    """
    id_sprint = request.POST['id_sprint']
    cancellation_reason = request.POST['cancellation_reason']

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.status = 'Cancelado'
    sprint.cancellation_reason = cancellation_reason
    sprint.save()

    return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


@permission_proj_required(UPermissionsProject.READ_SPRINT)
def sprint(request, id_project, id_sprint):
    """
    Retorna el documento HTML con la vista de un sprint dentro de un proyecto

    :param request
    :param id_project: id del proyecto actual, al que pertenece el sprint
    :param id_sprint: id del sprint que se quiere visualizar

    :return: documento HTML con la vista del sprint
    """
    context = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return render(request, 'sprint/base/app.html', context)


##################################################################
###################### SRPINT MEMBER #############################
##################################################################

@permission_proj_required(UPermissionsProject.READ_SPRINTMEMBER)
def members(request, id_project, id_sprint):
    """
    Muestra la lista de miembros de un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint actual, del que se quiere visualizar sus miembros

    :return: documento HTML con la lista de miembros del sprint
    """
    members = SprintMember.objects.filter(sprint_id=id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'members': members
    }

    return render(request, 'sprint/members/index.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINTMEMBER)
def add_member(request, id_project, id_sprint):
    """
    Devuelve la página para añadir un miembro a un sprint

    :param request:
    :param id_project: id del proyecto actual, al que pertenece el sprint
    :param id_sprint: id del sprint actual, al que se quiere añadir un miembro

    :return: Documento HTML para añadir miembros a un sprint
    """
    sprint = Sprint.objects.get(id=id_sprint)
    project = Project.objects.get(id=id_project)

    current_members = sprint.members.all()
    all_users_this_project = project.members.all()

    users_sprint = list(set(all_users_this_project) - set(current_members))

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'users_sprint': users_sprint
    }

    return render(request, 'sprint/members/create.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINTMEMBER)
def store_member(request, id_project, id_sprint):
    """
    Agrega un miembro a un sprint, con su respectiva carga horaria diaria

    :param request:
    :param id_project: id del proyecto actual, al que pertenece el sprint
    :param id_sprint: id del sprint actual, al que se quiere añadir un miembro

    :return: documento HTML para seguir agregando miembros al sprint
    """
    user_id = request.POST['user_id']
    workload = request.POST['workload']

    member = SprintMember.objects.create(sprint_id=id_sprint, user_id=user_id, workload=workload)

    messages.success(request, f'El miembro "{member.user.username}" se agrego al sprint con éxito')

    return redirect(reverse('sprints.members.add', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINTMEMBER)
def edit_member(request, id_project, id_sprint, member_id):
    member = SprintMember.objects.get(id=member_id)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'member': member
    }

    return render(request, 'sprint/members/edit.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINTMEMBER)
def update_member(request, id_project, id_sprint):
    member_id = request.POST['member_id']
    workload = request.POST['workload']

    member = SprintMember.objects.get(id=member_id)
    member.workload = workload

    member.save()

    return redirect(reverse('sprints.members.index', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


@permission_proj_required(UPermissionsProject.DELETE_SPRINTMEMBER)
def delete_member(request, id_project, id_sprint, member_id):
    sprint = Sprint.objects.get(id=id_sprint)
    member = SprintMember.objects.get(id=member_id)

    sprint.members.remove(member.user)

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.members.index', kwargs=kwargs), request)


@permission_proj_required(UPermissionsProject.READ_SPRINT_BACKLOG)
def sprint_backlog(request, id_project, id_sprint):
    sprint_backlog = UserStory.objects.filter(project_id=id_project, sprint_id=id_sprint).exclude(assigned_to=None)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'sprint_backlog': sprint_backlog
    }
    return render(request, 'sprint/sprint_backlog/index.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINT_BACKLOG)
def add_sprint_backlog(request, id_project, id_sprint):
    #agregamos los us no finalizados y ademas lo no existentes
    user_stories = UserStory.objects.get_us_non_finished(id_project=id_project).exclude(project_id=id_project,
                                                                                        sprint_id=id_sprint)
    members = get_sprint_member(id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_stories': user_stories,
        'members': members
    }
    return render(request, 'sprint/sprint_backlog/create.html', context)


@permission_proj_required(UPermissionsProject.CREATE_SPRINT_BACKLOG)
def store_sprint_backlog(request, id_project, id_sprint):
    id_user_story = request.POST['id_user_story']
    id_member = request.POST['id_member']

    user_story = UserStory.objects.get(id=id_user_story)
    member = SprintMember.objects.get(id=id_member)

    user_story.assigned_to = member
    user_story.sprint_id = id_sprint
    user_story.save()

    user_stories = get_user_stories(id_project)
    members = get_sprint_member(id_sprint)

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.sprint_backlog.add', kwargs=kwargs), request)


def get_user_stories(id_project):
    return UserStory.objects.filter(project_id=id_project, assigned_to=None)


def get_sprint_member(id_sprint):
    return SprintMember.objects.filter(sprint_id=id_sprint)


@permission_proj_required(UPermissionsProject.READ_SPRINT_BACKLOG)
def details_sprint_backlog(request, id_project, id_sprint, id_user_story):
    user_story = UserStory.objects.get(id=id_user_story)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_story': user_story
    }

    return render(request, 'sprint/sprint_backlog/details.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT_BACKLOG)
def edit_sprint_backlog(request, id_project, id_sprint, id_user_story):
    user_story = UserStory.objects.get(id=id_user_story)
    members = get_sprint_member(id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_story': user_story,
        'members': members
    }

    return render(request, 'sprint/sprint_backlog/edit.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT_BACKLOG)
def update_sprint_backlog(request, id_project, id_sprint):
    id_user_story = request.POST['id_user_story']
    id_member = request.POST['id_member']

    user_story = UserStory.objects.get(id=id_user_story)
    user_story.assigned_to_id = id_member
    user_story.save()

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.sprint_backlog.index', kwargs=kwargs), request)


@permission_proj_required(UPermissionsProject.DELETE_SPRINT_BACKLOG)
def delete_sprint_backlog(request, id_project, id_sprint, id_user_story):
    user_story = UserStory.objects.get(id=id_user_story)

    user_story.assigned_to = None
    user_story.sprint = None
    user_story.save()

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.sprint_backlog.index', kwargs=kwargs), request)
