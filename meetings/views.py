from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import Project
from meetings.models import Meeting


def index(request, id_project):
    project = Project.objects.get(id=id_project)
    meetings = project.meeting_set.all().order_by('-meeting_date')

    context = dict(meetings=meetings, id_project=id_project)
    return render(request, 'meetings/index.html', context)


def details(request, id_project, id):
    meeting = Meeting.objects.get(id=id)
    return render(request, 'meetings/details.html', {'id_project': id_project, 'meeting': meeting})


def create(request, id_project):
    return render(request, 'meetings/create.html', {'id_project': id_project})


def store(request, id_project):
    meeting_name = request.POST['name']
    meeting_date = request.POST['date']
    meeting_details = request.POST['details']
    meeting = Meeting.objects.create(
        project_id=id_project,
        meeting_name=meeting_name,
        meeting_details=meeting_details,
        meeting_date=meeting_date
    )
    messages.success(request, 'La reunión "' + meeting.meeting_name + '" se ha registrado correctamente')
    return redirect(reverse('meetings.create', kwargs={'id_project': id_project}), request)


def edit(request, id_project, id):
    return 0


def update(request, id_project, id):
    return 0


def destroy(request, id_project, id):
    return 0
