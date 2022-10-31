from datetime import date

import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from projects.decorators import permission_proj_required
from projects.models import Project
from user_story.models import UserStory
from utilities.UPermissionsProj import UPermissionsProject
from utilities.UProject import UProject
from utilities.USprint import USprint
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
    exists_planning = get_exists_planning(id_project, sprints)
    exists_execution = get_exists_execution(id_project, sprints)

    context = {
        'sprints': sprints,
        'id_project': id_project,
        'exists_planning': exists_planning,
        'exists_execution': exists_execution,
        'is_visible': is_visible_buttons(id_project=id_project)
    }

    print(f'exists_execution = {exists_execution} | is_visible = {is_visible_buttons(id_project=id_project)}')

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
    duration = int(request.POST['duration'])

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.sprint_name = name
    sprint.description = description

    new_capacity = get_all_workload(sprint) * duration
    new_available_capacity = new_capacity - get_accumulated(sprint)

    if duration < sprint.duration:
        if new_available_capacity < 0:
            messages.error(request,
                           "No se puede actualizar la duración del sprint, porque la estimacion de los US del sprint consumen toda la capacidad")
        else:
            sprint.capacity = new_capacity
            sprint.available_capacity = new_available_capacity
            sprint.duration = duration
            sprint.save()

            messages.success(request, "Se actualizó con éxito")
    else:
        sprint.capacity = new_capacity
        sprint.available_capacity = new_available_capacity
        sprint.duration = duration
        sprint.save()

        messages.success(request, "Se actualizó con éxito")

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.edit_sprint', kwargs=kwargs), request)


def get_all_workload(sprint):
    members = SprintMember.objects.filter(sprint_id=sprint.id)

    all_workload = 0

    for member in members:
        all_workload += member.workload

    return all_workload


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
    is_all_no_finished = UserStory.objects.get_us_non_finished(id_project=id_project).filter(
        sprint_id=id_sprint).exists()

    if not is_all_no_finished:
        context = {
            'id_project': id_project,
            'sprint': sprint
        }
        return render(request, 'sprint/cancel_sprint.html', context)
    else:
        messages.error(request, f'No se puede cancelar un sprint que no tenga sus US en estados finales')
        return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


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
    sprint.status = USprint.STATUS_CANCELED
    sprint.cancellation_reason = cancellation_reason
    sprint.save()
    messages.success(request, f'Se canceló el sprint {sprint.sprint_name} con éxito')

    return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


# @permission_proj_required(UPermissionsProject.READ_SPRINT)
def dashboard(request, id_project, id_sprint):
    """
    Devuelve el dashboard del sprint

    :param id_project: id del proyecto actual
    :param request

    :return: documento HTML
    """
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_sprint': id_sprint,
        'id_project': id_project,
        'sprint': sprint
    }

    return render(request, 'sprint/dashboard.html', context)


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

    team_capacity = 0

    for member in members:
        team_capacity += member.workload

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'members': members,
        'team_capacity': team_capacity,
        'is_visible': is_visible_buttons(id_sprint=id_sprint)
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
    workload = int(request.POST['workload'])

    member = SprintMember.objects.create(sprint_id=id_sprint, user_id=user_id, workload=workload)

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.capacity += workload * sprint.duration

    sprint.available_capacity = get_available_capacity(sprint)

    sprint.save()

    messages.success(request, f'El miembro "{member.user.username}" se agrego al sprint con éxito')

    return redirect(reverse('sprints.members.add', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINTMEMBER)
def edit_member(request, id_project, id_sprint, member_id):
    """
    Muestra los datos para la edición de un miembro de un Sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece el miembro
    :param member_id: id del miembro de sprint a ser editado

    :return: documento HTML para la edición de los datos
    """

    member = SprintMember.objects.get(id=member_id)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'member': member
    }

    return render(request, 'sprint/members/edit.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINTMEMBER)
def update_member(request, id_project, id_sprint):
    """
    Guarda los cambios realizados sobre un miembro de un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece el miembro

    :return: documento HTML con la lista de miembros del sprint, con los datos actualizados
    """
    member_id = request.POST['member_id']
    workload = int(request.POST['workload'])

    sprint = Sprint.objects.get(id=id_sprint)
    member = SprintMember.objects.get(id=member_id)

    old_capacity = sprint.capacity
    new_capacity = old_capacity - member.workload * sprint.duration + workload * sprint.duration
    new_available_capacity = new_capacity - get_accumulated(sprint)

    if new_available_capacity <= sprint.available_capacity:
        messages.error(request, "No se puede dar menos horas por el consumo de horas de los US")
    else:
        member.workload = workload
        sprint.capacity = new_capacity
        sprint.available_capacity = get_available_capacity(sprint)
        member.save()
        sprint.save()
        messages.success(request, "Se actualizó correctamente")

    return redirect(reverse('sprints.members.index', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


@permission_proj_required(UPermissionsProject.DELETE_SPRINTMEMBER)
def delete_member(request, id_project, id_sprint, member_id):
    """
    Elimina un miembro de un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece el miembro
    :param member_id: id del miembro de sprint a eliminado

    :return: documento HTML con la lista de miembros del sprint
    """

    sprint = Sprint.objects.get(id=id_sprint)
    member = SprintMember.objects.get(id=member_id)
    if not UserStory.objects.filter(assigned_to=member).exists():
        workload = member.workload

        sprint.members.remove(member.user)

        sprint.capacity = sprint.capacity - sprint.duration * workload
        sprint.available_capacity = get_available_capacity(sprint)
        sprint.save()
    else:
        messages.error(request, f"No se puede eliminar al miembro {member.user.email} porque esta asignado a un US")

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.members.index', kwargs=kwargs), request)


@permission_proj_required(UPermissionsProject.READ_SPRINT_BACKLOG)
def sprint_backlog(request, id_project, id_sprint):
    """
    Muestra el backlog de un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint del que se va a visualizar su backlog

    :return: Documento HTML con el backlog del sprint
    """
    sprint_backlog = UserStory.objects.filter(project_id=id_project, sprint_id=id_sprint).exclude(assigned_to=None)
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'sprint_backlog': sprint_backlog,
        'sprint': sprint,
        'is_visible': is_visible_buttons(id_sprint=id_sprint)
    }
    return render(request, 'sprint/sprint_backlog/index.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT_BACKLOG)
def add_sprint_backlog(request, id_project, id_sprint):
    """
    Muestra la página para agregar historias de usuario a un sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que se va a agregar la historia de usuario

    :return: Documento HTML donde se puede elegir la historia de usuario a ser
    agregada al sprint y el responsable de la misma
    """
    members = get_sprint_member(id_sprint)
    if members.count() > 0:
        sprint = Sprint.objects.get(id=id_sprint)
        # user_stories = UserStory.objects.get_us_no_assigned(id_project, id_sprint)
        backlog = UserStory.objects.get_us_non_finished(id_project) \
            .filter(sprint__isnull=True) \
            .order_by('final_priority').reverse()
        sprint_backlog = UserStory.objects.get_us_non_finished(id_project) \
            .filter(sprint_id=id_sprint) \
            .order_by('final_priority').reverse()

        context = {
            'id_project': id_project,
            'id_sprint': id_sprint,
            'backlog': backlog,
            'sprint_backlog': sprint_backlog,
            'members': members,
            'sprint': sprint
        }
        return render(request, 'sprint/sprint_backlog/create.html', context)
    else:
        messages.error(request, 'No se puede agregar un US si no existe miembros en el Sprint')
        return redirect(
            reverse('sprints.sprint_backlog.index', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
            request)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT_BACKLOG)
def store_sprint_backlog(request, id_project, id_sprint):
    """
    Guarda la historia de usuario en el backlog de un sprint con su respectivo encargado y
    retorna la página para seguir agregad historias de usuario al sprint

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que se va a agregar la historia de usuario

    :return: Documento HTML donde se puede elegir la historia de usuario a ser
    agregada al sprint y el responsable de la misma
    """
    id_user_story = request.POST['id_user_story']
    id_member = request.POST['id_member']

    user_story = UserStory.objects.get(id=id_user_story)
    member = SprintMember.objects.get(id=id_member)

    user_story.assigned_to = member
    user_story.sprint_id = id_sprint
    user_story.save()

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.available_capacity -= user_story.estimation_time
    sprint.save()

    context = {
        'available_capacity': sprint.available_capacity,
        'status': 200,
        'message': f'El User Story {user_story.title} fue agregado correctamente'
    }
    return JsonResponse(context)


def get_user_stories(id_project):
    """
    Función para obtener todas las historias de usuario de un proyecto
    y que no tengan un encargado asignado

    :param id_project: id del proyecto del que se quiere obtener las historias de usuario

    :return: lista de las historias de usuario del proyecto
    """
    return UserStory.objects.filter(project_id=id_project, assigned_to=None)


def get_sprint_member(id_sprint):
    """
    Función para obtener la lista de miembros de un sprint

    :param id_sprint: id del sprint del que se quiere obtener sus miembros

    :return: lista de miembros del sprint
    """
    return SprintMember.objects.filter(sprint_id=id_sprint)


@permission_proj_required(UPermissionsProject.READ_SPRINT_BACKLOG)
def details_sprint_backlog(request, id_project, id_sprint, id_user_story):
    """
    Muestra los detalles de una historia de usuario del sprint backlog

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece la historia de usuario
    :param id_user_story: id de la historia de usuario cuyos detalles se van a visualizar

    :return: documento HTML con los detalles de la historia de usuario
    """

    user_story = UserStory.objects.get(id=id_user_story)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_story': user_story
    }

    return render(request, 'sprint/sprint_backlog/details.html', context)


@permission_proj_required(UPermissionsProject.UPDATE_SPRINT_BACKLOG)
def edit_sprint_backlog(request, id_project, id_sprint, id_user_story):
    """
    Muestra la página para editar los detalles de una historia de usuario dentro del sprint backlog

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece la historia de usuario
    :param id_user_story: id de la historia de usuario cuyos detalles se quiere editar

    :return: Documento HTML para editar los detalles de la historia de usuario
    """
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
    """
    Guarda los cambios realizados a la historia de usuario dentro del sprint backlog

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece la historia de usuario

    :return: Documento HTML del backlog del sprint
    """
    id_user_story = request.POST['id_user_story']
    id_member = request.POST['id_member']
    estimation_time = int(request.POST['estimation_time'])

    sprint = Sprint.objects.get(id=id_sprint)

    user_story = UserStory.objects.get(id=id_user_story)
    user_story.assigned_to_id = id_member

    new_available_capacity = sprint.available_capacity + user_story.estimation_time - estimation_time

    if estimation_time > user_story.estimation_time:
        if new_available_capacity < 0:
            messages.error(request, "No se puede actualizar a una estimación que consuma toda la capacidad del sprint")
        else:
            sprint.available_capacity = new_available_capacity
            sprint.save()

            user_story.estimation_time = estimation_time
            user_story.save()

            messages.success(request, "Se actualizó correctamente")
    else:
        sprint.available_capacity = new_available_capacity
        sprint.save()

        user_story.estimation_time = estimation_time
        user_story.save()

        messages.success(request, "Se actualizó correctamente")

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.sprint_backlog.index', kwargs=kwargs), request)


@permission_proj_required(UPermissionsProject.DELETE_SPRINT_BACKLOG)
def delete_sprint_backlog(request, id_project, id_sprint):
    """
    Elimina una historia de usuario del sprint backlog

    :param request:
    :param id_project: id del proyecto al que pertenece el sprint
    :param id_sprint: id del sprint al que pertenece la historia de usuario
    :param id_user_story: id de la historia de usuario que se quiere eliminar

    :return: Documento HTML del backlog del sprint
    """
    id_user_story = request.POST['user_story_id']
    user_story = UserStory.objects.get(id=id_user_story)

    user_story.assigned_to = None
    user_story.sprint = None
    user_story.save()

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.available_capacity += user_story.estimation_time
    sprint.save()

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }
    # lanzara un error si no es un ajax request lo cual significa que se llamo desde el index
    try:
        isAjax = request.POST['is_ajax']
        context = {
            'available_capacity': sprint.available_capacity,
            'status': 200,
            'message': f'El User Story {user_story.title} fue desadjuntado correctamente'
        }
        return JsonResponse(context)
    except:
        return redirect(reverse('sprints.sprint_backlog.index', kwargs=kwargs), request)


def get_available_capacity(sprint):
    return sprint.capacity - get_accumulated(sprint)


def get_accumulated(sprint):
    user_stories = UserStory.objects.filter(sprint_id=sprint.id)
    accumulated = 0
    for user_story in user_stories:
        accumulated += user_story.estimation_time

    return accumulated


@permission_proj_required(UPermissionsProject.INIT_SPRINT)
def init_sprint(request, id_project, id_sprint):
    project = Project.objects.get(id=id_project)
    sprint = Sprint.objects.get(id=id_sprint)

    if project.status == UProject.STATUS_IN_EXECUTION:
        if SprintMember.objects.filter(sprint_id=id_sprint).exists():
            if UserStory.objects.filter(sprint_id=id_sprint).exists():
                switch_to_started_sprint(sprint)
                messages.success(request, 'El sprint inició con éxito')
            else:
                messages.error(request, 'El sprint no puede iniciar hasta que tenga al menos un US')
        else:
            messages.error(request, 'El sprint no puede iniciar hasta que tenga al menos un miembro')
    else:
        messages.error(request, 'El sprint no puede iniciar hasta que el proyecto haya iniciado')

    kwargs = {
        'id_project': id_project
    }

    return redirect(reverse('sprints.index', kwargs=kwargs), request)


def get_exists_planning(id_project, sprints):
    for sprint in sprints:
        if sprint.status == USprint.STATUS_PENDING:
            return True

    return False


def get_exists_execution(id_project, sprints):
    exists_execution = False
    for sprint in sprints:
        if sprint.status == USprint.STATUS_IN_EXECUTION:
            return True

    return False


def switch_to_started_sprint(sprint):
    sprint.status = USprint.STATUS_IN_EXECUTION
    sprint.start_at = date.today()
    print(sprint.start_at)
    s = pd.date_range(start=sprint.start_at, periods=sprint.duration, freq='B')
    df = pd.DataFrame(s, columns=['fecha'])
    end_at = str(df.iloc[-1]["fecha"]).split(' ')[0]
    sprint.end_at = end_at
    sprint.save()


def is_visible_buttons(id_project=None, id_sprint=None):
    if id_project is not None:
        project = Project.objects.get(id=id_project)

        if project.status == UProject.STATUS_CANCELED or project.status == UProject.STATUS_FINISHED:
            return False

        return True
    else:
        sprint = Sprint.objects.get(id=id_sprint)

        if sprint.status == UProject.STATUS_CANCELED or sprint.status == USprint.STATUS_FINISHED:
            return False

        return True
