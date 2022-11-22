from django.shortcuts import render

from projects.models import Project


def index(request, id_project):

    project = Project.objects.get(id=id_project)
    meetings = project.meeting_set.all().order_by('id')

    context = dict(meetings=meetings, id_project=id_project)
    return render(request, 'meetings/index.html', context)
