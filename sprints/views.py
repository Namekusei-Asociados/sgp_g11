from django.shortcuts import render
from .models import Sprint
from accounts.models import User


# Create your views here.


def index(request):
    """
    Devuelve la lista de sprints del proyecto

    :param request:

    :return: documento HTML
    """
    sprints = Sprint.objects.all()
    return render(request, 'sprint/index.html', {'sprints': sprints})


def create_sprint(request):
    user_stories = User.objects.all()
    user_stories = filter(lambda x: x.role_sys != 'visitor' and not x.is_staff, user_stories)
    return render(request, 'sprint/create_sprint.html', {"user_stories": user_stories})


def validate_create_sprint(request):
    sprint_name = request.POST("")
    return None
