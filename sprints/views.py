from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import Project
from user_story.models import UserStory
from .models import Sprint, SprintMember


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

    context = {
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


def edit_sprint(request, id_project, id_sprint):
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_project': id_project,
        'sprint': sprint
    }

    return render(request, 'sprint/edit_sprint.html', context)


def validate_edit_sprint(request, id_project):
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


def cancel_sprint(request, id_project, id_sprint):
    sprint = Sprint.objects.get(id=id_sprint)

    context = {
        'id_project': id_project,
        'sprint': sprint
    }

    return render(request, 'sprint/cancel_sprint.html', context)


def validate_cancel_sprint(request, id_project):
    id_sprint = request.POST['id_sprint']
    cancellation_reason = request.POST['cancellation_reason']

    sprint = Sprint.objects.get(id=id_sprint)
    sprint.status = 'Cancelado'
    sprint.cancellation_reason = cancellation_reason
    sprint.save()

    return redirect(reverse('sprints.index', kwargs={'id_project': id_project}), request)


def sprint(request, id_project, id_sprint):
    context = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return render(request, 'sprint/base/app.html', context)


def members(request, id_project, id_sprint):
    members = SprintMember.objects.filter(sprint_id=id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'members': members
    }

    return render(request, 'sprint/members/index.html', context)


def add_member(request, id_project, id_sprint):
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


def store_member(request, id_project, id_sprint):
    user_id = request.POST['user_id']
    workload = request.POST['workload']

    member = SprintMember.objects.create(sprint_id=id_sprint, user_id=user_id, workload=workload)

    messages.success(request, f'El miembro {member.user.username} se agrego al proyecto con exito')

    return redirect(reverse('sprints.members.add', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


def edit_member(request, id_project, id_sprint, member_id):
    member = SprintMember.objects.get(id=member_id)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'member': member
    }

    return render(request, 'sprint/members/edit.html', context)


def update_member(request, id_project, id_sprint):
    member_id = request.POST['member_id']
    workload = request.POST['workload']

    member = SprintMember.objects.get(id=member_id)
    member.workload = workload

    member.save()

    return redirect(reverse('sprints.members.index', kwargs={'id_project': id_project, 'id_sprint': id_sprint}),
                    request)


def delete_member(request, id_project, id_sprint, member_id):
    sprint = Sprint.objects.get(id=id_sprint)
    member = SprintMember.objects.get(id=member_id)

    sprint.members.remove(member.user)

    kwargs = {
        'id_project': id_project,
        'id_sprint': id_sprint
    }

    return redirect(reverse('sprints.members.index', kwargs=kwargs), request)


def sprint_backlog(request, id_project, id_sprint):
    sprint_backlog = UserStory.objects.filter(project_id=id_project, sprint_id=id_sprint).exclude(assigned_to=None)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'sprint_backlog': sprint_backlog
    }
    return render(request, 'sprint/sprint_backlog/index.html', context)


def add_sprint_backlog(request, id_project, id_sprint):
    user_stories = get_user_stories(id_project)
    members = get_sprint_member(id_sprint)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_stories': user_stories,
        'members': members
    }
    return render(request, 'sprint/sprint_backlog/create.html', context)


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


def details_sprint_backlog(request, id_project, id_sprint, id_user_story):
    user_story = UserStory.objects.get(id=id_user_story)

    context = {
        'id_project': id_project,
        'id_sprint': id_sprint,
        'user_story': user_story
    }

    return render(request, 'sprint/sprint_backlog/details.html', context)


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
