from django.shortcuts import render
from .models import Sprint
from accounts.models import User


# Create your views here.


def index(request, id_project):
    """
    Devuelve la lista de sprints del proyecto

    :param request:

    :return: documento HTML
    """
    sprints = Sprint.objects.all()
    context = {'sprints': sprints, 'id_project': id_project}
    return render(request, 'sprint/index.html', context)


def create_sprint(request, id_project):
    user_stories = User.objects.all()
    user_stories = filter(lambda x: x.role_sys != 'visitor' and not x.is_staff, user_stories)
    context = {"user_stories": user_stories, 'id_project': id_project}
    return render(request, 'sprint/create_sprint.html', context)


def validate_create_sprint(request):
    sprint_name = request.POST("")
    return None
