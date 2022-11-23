from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import Project
from meetings.models import Meeting


def index(request, id_project):
    """
    Muestra la lista de reuniones de un proyecto

    :param request: request
    :param id_project: id del proyecto al que pertenecen las reuniones

    :return: Documento HTML con la lista de reuniones
    """
    project = Project.objects.get(id=id_project)
    meetings = project.meeting_set.all().order_by('-meeting_date')

    context = dict(meetings=meetings, id_project=id_project)
    return render(request, 'meetings/index.html', context)


def details(request, id_project, id):
    """
    Muestra los detalles de una reunión

    :param request: request
    :param id_project: id del proyecto al que pertenece la reunión
    :param id: id de la reunión

    :return: documento HTML con los detalles de la reunión
    """
    meeting = Meeting.objects.get(id=id)
    return render(request, 'meetings/details.html', {'id_project': id_project, 'meeting': meeting})


def create(request, id_project):
    """
    Muestra el formulario para crear una reunión

    :param request: request
    :param id_project: id del proyecto en el que se creará la reunión

    :return: documento HTML con el formulario para crear una reunión
    """
    return render(request, 'meetings/create.html', {'id_project': id_project})


def store(request, id_project):
    """
    Crea y guarda una reunión en la base de datos

    :param request: request
    :param id_project: id del proyecto en el que se creará la reunión

    :return: Documento HTML con la lista de reuniones
    """
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
    return redirect(reverse('meetings.index', kwargs={'id_project': id_project}), request)


def edit(request, id_project, id):
    """
    Muetsra el formulario para editar una reunión

    :param request: request
    :param id_project: id del proyecto al que pertenece la reunión
    :param id: id de la reunión

    :return: Documento HTML con el formulario para editar una reunión
    """
    meeting = Meeting.objects.get(id=id)
    return render(request, 'meetings/edit.html', {'id_project': id_project, 'meeting': meeting})


def update(request, id_project, id):
    """
    Actualiza los detalles de una reunión en la base de datos

    :param request: request
    :param id_project: id del proyecto al que pertenece la reunión
    :param id: id de la reunión

    :return: Documento HTML con la lista de reuniones
    """
    meeting_name = request.POST['name']
    meeting_date = request.POST['date']
    meeting_details = request.POST['details']
    meeting = Meeting.objects.get(id=id)
    meeting.meeting_name = meeting_name
    meeting.meeting_date = meeting_date
    meeting.meeting_details = meeting_details
    meeting.save()
    messages.success(request, 'La reunión "' + meeting.meeting_name + '" se ha actualizado correctamente')
    return redirect(reverse('meetings.index', kwargs={'id_project': id_project}), request)


def destroy(request, id_project, id):
    """
    Elimina una reunión de la base de datos

    :param request: request
    :param id_project: id del proyecto al que pertenece la reunión
    :param id: id de la reunión

    :return: Documento HTML con la lista de reuniones
    """
    meeting = Meeting.objects.get(id=id)
    meeting.delete()
    messages.success(request, 'La reunión "' + meeting.meeting_name + '" se ha eliminado correctamente')
    return redirect(reverse('meetings.index', kwargs={'id_project': id_project}), request)
