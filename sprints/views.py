from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import ProjectMember
from user_story.models import UserStory
from .models import Sprint


# Create your views here.


def index(request, id_project):
    """
    Devuelve la lista de sprints del proyecto

    :param id_project:
    :param request:

    :return: documento HTML
    """
    sprints = Sprint.objects.filter(project_id=id_project)
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


def create_sprint(request, id_project):
    """
    Devuelve el template para crear un nuevo sprint

    :param request:
    :param id_project: id del proyecto en el cual se debe crear el sprint

    :return: documento HTML
    """
    user_stories = UserStory.objects.filter(project_id=id_project, sprint_id=None)
    projectMembers = ProjectMember.objects.filter(project_id=id_project)

    context = {
        'projectMembers': projectMembers,
        'user_stories': user_stories,
        'id_project': id_project
    }

    return render(request, 'sprint/create_sprint.html', context)


def validate_create_sprint(request, id_project):
    """
    Función para guardar un nuevo sprint

    :param request:
    :param id_project: id del proyecto en el cual se crea el sprint

    :return: template para crear un nuevo sprint
    """
    sprint_name = request.POST['sprint_name']
    duration = request.POST['duration']

    Sprint.objects.create(sprint_name=sprint_name, duration=duration,
                          number=numbersSprint(id_project), project_id=id_project)

    message = 'El sprint "' + sprint_name + '" fue creada con éxito'
    messages.success(request, message)

    return redirect(reverse('sprints.create_sprint', kwargs={'id_project': id_project}), request)


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
