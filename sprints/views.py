import pandas as pd
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from django.shortcuts import render, redirect
from django.urls import reverse
from sphinx.jinja2glue import idgen

from projects.models import Project, ProjectMember
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
    context = {
        'sprints': sprints,
        'id_project': id_project
    }

    return render(request, 'sprint/index.html', context)


def create_sprint(request, id_project):
    user_stories = UserStory.objects.filter(project_id=id_project, sprint_id=None)
    projectMembers = ProjectMember.objects.filter(project_id=id_project)

    context = {
        'projectMembers': projectMembers,
        'user_stories': user_stories,
        'id_project': id_project
    }

    return render(request, 'sprint/create_sprint.html', context)


def validate_create_sprint(request, id_project):
    sprint_name = request.POST['sprint_name']
    start_at = request.POST['start_at']
    end_at = request.POST['end_at']
    duration = pd.bdate_range(start=start_at, end=end_at).size
    user_stories = request.POST.getlist('user_stories[]')

    sprint = Sprint.objects.create(sprint_name=sprint_name, start_at=start_at, end_at=end_at, duration=duration,
                                   number=numbersSprint(id_project), project_id=id_project)

    for user_story in user_stories:
        us = UserStory.objects.get(id=int(user_story))
        us.sprint = sprint
        us.save()

    return redirect(reverse('sprints.create_sprint', kwargs={'id_project': id_project}), request)


def daterange(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))


def numbersSprint(id_project):
    return Sprint.objects.filter(project_id=id_project).count() + 1
