from django.shortcuts import render, redirect
from django.urls import reverse


from accounts.models import User
from projects.models import ProjectMember
from user_story.models import UserStory


# Create your views here.
def create_user_story(request, id_project):
    users = User.objects.filter(projectmember__project_id=id_project)

    context = {
        'id_project': id_project,
        'users': users
    }
    return render(request, 'user_story/create_user_story.html', context)


def validate_create_user_story(request, id_project):
    title = request.POST['title']
    description = request.POST['description']
    business_value = int(request.POST['business_value'])
    technical_priority = int(request.POST['technical_priority'])
    id_user = int(request.POST['assigned_to'])
    us_type = request.POST['us_type']
    estimation_time = int(request.POST['estimation_time'])
    project_member = ProjectMember.objects.get(user_id=id_user, project_id=id_project)

    UserStory.objects.create(
        title=title, description=description,
        business_value=business_value, technical_priority=technical_priority,
        estimation_time=estimation_time, assigned_to=project_member,
        project_id=id_project
    )

    return redirect(reverse('user_story.create_user_story', kwargs={'id_project': id_project}), request)


def edit_user_story(request):
    return None


def validate_edit_user_story(request):
    return None


def cancel_user_story(request):
    return None


def validate_cancel_user_story(request):
    return None


def backlog(request, id_project):
    return render(request, 'user_story/backlog.html', {'id_project': id_project})
