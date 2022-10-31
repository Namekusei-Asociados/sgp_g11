from itertools import chain

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import User
from projects.decorators import permission_proj_required
from projects.models import Project
from type_us.models import TypeUS
from user_story.models import UserStory
from utilities.UPermissionsProj import UPermissionsProject
from utilities.UProject import UProject


# Create your views here.
@permission_proj_required(UPermissionsProject.CREATE_US)
def create_user_story(request, id_project):
    """
    Retorna el template para crear una nueva historia de usuario

    :param request:
    :param id_project: id del proyecto en el que se crea la historia de usuario

    :return: template para crear una nueva historia de usuario
    """
    context = get_user_story_context(id_project)

    return render(request, 'user_story/create_user_story.html', context)


@permission_proj_required(UPermissionsProject.CREATE_US)
def validate_create_user_story(request, id_project):
    """
    Valida los datos y crea la historia de usuario

    :param request:
    :param id_project: id del proyecto en el que se crea la historia de usuario

    :return: template para crear una nueva historia de usuario
    """
    title = request.POST['title']
    description = request.POST['description']
    business_value = int(request.POST['business_value'])
    technical_priority = int(request.POST['technical_priority'])
    final_priority = 0.6 * business_value + 0.4 * technical_priority
    us_type = request.POST['us_type']
    estimation_time = int(request.POST['estimation_time'])

    # obetenemos el primer estado del tipo de US
    initial_status = UserStory.objects.get_initial_status(id_type_us=us_type)

    UserStory.objects.create(
        title=title, description=description,
        business_value=business_value, technical_priority=technical_priority,
        estimation_time=estimation_time, final_priority=final_priority,
        project_id=id_project, us_type_id=us_type, current_status=initial_status,
    )

    message = 'La historia de usuario "' + title + '" fue creada con éxito'
    messages.success(request, message)

    return redirect(reverse('user_story.create_user_story', kwargs={'id_project': id_project}), request)


@permission_proj_required(UPermissionsProject.UPDATE_US)
def edit_user_story(request, id_project, id_user_story):
    """
    Retorna el template para editar una historia de usuario

    :param request:
    :param id_project: id del proyecto al que pertenece la historia de usuario

    :return: template para editar una historia de usuario
    """
    context = get_user_story_context(id_project)

    # user_story_id = int(request.POST.get('id_user_story'))
    user_story = UserStory.objects.get(id=id_user_story)
    context['user_story'] = user_story

    return render(request, 'user_story/edit_user_story.html', context)


def get_user_story_context(id_project):
    """
    Retorna el contexto a ser enviado para crear o editar una historia de usuario

    :param id_project: id del proyecto al que pertenece o pertenecerá la historia de usuario

    :return: contexto a ser enviado
    """
    users = User.objects.filter(projectmember__project_id=id_project)

    try:
        type_us = TypeUS.objects.filter(project_id=id_project)
    except TypeUS.DoesNotExist:
        type_us = None

    if not type_us.exists():
        context = {
            'id_project': id_project,
            'users': users,
            'type_us': None
        }
    else:
        context = {
            'id_project': id_project,
            'users': users,
            'type_us': type_us
        }

    return context


@permission_proj_required(UPermissionsProject.UPDATE_US)
def validate_edit_user_story(request, id_project):
    """
    Actualiza los datos de la historia de usuario que se está editando

    :param request:
    :param id_project: id del proyecto actual, al que pertenece la historia de usuario

    :return: formulario de edición de la historia de usuario, pero con los datos ya actualizados
    """
    title = request.POST['title']
    description = request.POST['description']

    user_story_id = int(request.POST.get('id_user_story'))
    user_story = UserStory.objects.get(id=user_story_id)
    user_story.title = title
    user_story.description = description
    user_story.save()

    message = 'La historia de usuario "' + user_story.title + '" fue actualizada con éxito'
    messages.success(request, message)

    return redirect(
        reverse('user_story.edit_user_story', kwargs={'id_project': id_project, 'id_user_story': user_story_id}),
        request)


@permission_proj_required(UPermissionsProject.CANCEL_US)
def cancel_user_story(request, id_project, id_user_story):
    """
    Devuelve un template solicitando el motivo de la cancelación del US

    :param request
    :param id_project: id del proyecto al que pertenece el US a ser cancelado
    :param id_user_story: id del US a ser cancelado

    :return: template para ingresar el motivo de la cancelación del US
    """
    us = UserStory.objects.get(id=id_user_story)

    context = {
        'id_project': id_project,
        'us': us
    }

    return render(request, 'user_story/cancel_user_story.html', context)


def validate_cancel_user_story(request, id_project):
    """
    Guarda el motivo de la cancelación de un US y realiza la
    actualización de su estado a "canceled"

    :param request
    :param id_project: id del proyecto actual, al que pertenece el US a ser cancelado

    :return: documento HTML del backlog
    """
    id_us = request.POST['id_us']
    cancellation_reason = request.POST['cancellation_reason']

    us = UserStory.objects.get(id=id_us)
    us.cancellation_reason = cancellation_reason
    us.current_status = 'canceled'

    us.save()

    return redirect(reverse('user_story.backlog', kwargs={'id_project': id_project}), request)


@permission_proj_required(UPermissionsProject.READ_US)
def backlog(request, id_project):
    """
    Retorna el documento HTML del backlog de un proyecto

    :param request:
    :param id_project: id del proyecto del que se quiere su backlog

    :return: documento HTML del backlog de un proyecto
    """
    user_stories_data = UserStory.objects.filter(project_id=id_project)
    # dividimos entre estados finales y no finales
    final_us = UserStory.objects.get_us_finished(id_project=id_project)
    not_final_us = UserStory.objects.get_us_non_finished(id_project=id_project)
    user_stories = chain(not_final_us, final_us)

    context = {
        'id_project': id_project,
        'user_stories': user_stories,
        'is_visible': is_visible_buttons(id_project)
    }

    return render(request, 'user_story/backlog.html', context)


def details_user_story(request, id_project, id_user_story):
    """
    Devuelve un documento HTML donde se pueden visualizar todos los
    detalles de una historia de usuario

    :param request
    :param id_project: id del proyecto al que pertenece la historia de usuario
    :param id_user_story: id de la historia de usuario de la cual se quiere visualizar sus detalles

    :return: Documento HTML con los detalles de la historia de usuario
    """
    user_story = UserStory.objects.get(id=id_user_story)

    context = {
        'id_project': id_project,
        'user_story': user_story
    }

    return render(request, 'user_story/details_user_story.html', context)


def is_visible_buttons(id_project):
    project = Project.objects.get(id=id_project)

    if project.status == UProject.STATUS_CANCELED or project.status == UProject.STATUS_FINISHED:
        return False

    return True


def history(request, id_project, id_user_story):
    """
    Depsliega ventana de historial propio del US

    :param request:
    :param id_project: id del proyecto
    :param id_user_story: id del US a mirar el historial

    :return: Documento HTML
    """
    user_story = UserStory.objects.get(id=id_user_story)
    # new_record=user_story.history.first()
    # old_record = user_story.history.all()
    # for record in old_record:
    #     ant=record.previous()
    #     historical = new_record.diff_against(record)
    #     for change in historical.changes:
    #         print("{} changed from {} to {}".format(change.field, change.old, change.new))
    if request.method == 'POST':
        id_history = request.POST.get('id_history')
        print(f'id_history: {id_history}')
        h = user_story.history.get(history_id=id_history)

        h.instance.save()
        message = 'La historia de usuario "' + h.title + '" fue actualizada con éxito'
        messages.success(request, message)

        return redirect(
            reverse('user_story.history', kwargs={'id_project': id_project, 'id_user_story': id_user_story}),
            request)
    context = {
        'id_project': id_project,
        'user_story': user_story,
        'historical': user_story.history.all()
    }
    return render(request, 'user_story/history.html', context)


def restore(request):
    pass
