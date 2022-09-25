from django.shortcuts import render


# Create your views here.
def create_user_story(request, id_project):
    return render(request, 'user_story/create_user_story.html', {'id_project': id_project})


def validate_create_user_story(request):
    return None


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
