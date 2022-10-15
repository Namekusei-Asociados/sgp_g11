from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from accounts.models import User
from projects.models import ProjectMember
from type_us.models import TypeUS
from user_story.models import UserStory
from projects.decorators import permission_proj_required
from utilities.UPermissionsProj import UPermissionsProject


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
    # id_user = int(request.POST['assigned_to'])
    us_type = request.POST['us_type']
    estimation_time = int(request.POST['estimation_time'])
    # project_member = ProjectMember.objects.get(user_id=id_user, project_id=id_project)

    UserStory.objects.create(
        title=title, description=description,
        business_value=business_value, technical_priority=technical_priority,
        estimation_time=estimation_time,
        # assigned_to=project_member,
        project_id=id_project, us_type_id=us_type
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
    Actualiza la historia de usuario que debe ser editada

    :param request:
    :param id_project: id del proyecto actual, al que pertenece la historia de usuario

    :return: formulario de edición de la historia de usuario, pero con los datos ya actualizados
    """
    title = request.POST['title']
    description = request.POST['description']
    business_value = int(request.POST['business_value'])
    technical_priority = int(request.POST['technical_priority'])
    # id_user = int(request.POST['assigned_to'])
    # us_type = request.POST['us_type']
    estimation_time = int(request.POST['estimation_time'])
    # project_member = ProjectMember.objects.get(user_id=id_user, project_id=id_project)

    user_story_id = int(request.POST.get('id_user_story'))
    user_story = UserStory.objects.get(id=user_story_id)

    user_story.title = title
    user_story.description = description
    user_story.business_value = business_value
    user_story.technical_priority = technical_priority
    # user_story.assigned_to = project_member
    # user_story.us_type_id = us_type
    user_story.estimation_time = estimation_time
    user_story.save()

    message = 'La historia de usuario "' + user_story.title + '" fue actualizada con éxito'
    messages.success(request, message)

    return redirect(
        reverse('user_story.edit_user_story', kwargs={'id_project': id_project, 'id_user_story': user_story_id}),
        request)


@permission_proj_required(UPermissionsProject.CANCEL_US)
def cancel_user_story(request, id_project):
    return None


def validate_cancel_user_story(request):
    return None


@permission_proj_required(UPermissionsProject.READ_US)
def backlog(request, id_project):
    """
    Retorna el template del backlog de un proyecto

    :param request:
    :param id_project: id del proyecto del que se quiere su backlog

    :return: template del backlog de un proyecto
    """
    user_stories = UserStory.objects.filter(project_id=id_project)
    context = {
        'id_project': id_project,
        'user_stories': user_stories
    }
    return render(request, 'user_story/backlog.html', context)


def is_final_status(id_us):
    user_story = UserStory.objects.get(id=id_us)
    final_status = TypeUS.objects.get_final_status(id=user_story.us_type_id)

    return user_story.current_status == final_status
