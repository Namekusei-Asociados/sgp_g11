import datetime

from django.shortcuts import render
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
import pandas as pd

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
    context = {
        'sprints': sprints,
        'id_project': id_project
    }

    return render(request, 'sprint/index.html', context)


def create_sprint(request, id_project):
    user_stories = UserStory.objects.filter(project_id=id_project)
    context = {
        "user_stories": user_stories,
        'id_project': id_project
    }

    return render(request, 'sprint/create_sprint.html', context)


def validate_create_sprint(request, id_project):
    sprint_name = request.POST['sprint_name']
    capacity = request.POST['capacity']
    start_at = request.POST['start_at']
    end_at = request.POST['end_at']
    duration = pd.bdate_range(start=start_at, end=end_at).size

    user_stories = request.POST.getlist('user_stories[]')

    return None


def daterange(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR))
