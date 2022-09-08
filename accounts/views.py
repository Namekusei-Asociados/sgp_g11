from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User


@login_required()
def home(request):
    user = request.user
    if user.role_sys == 'visitor':
        return render(request, 'visitor.html')
    else:
        users = User.objects.all()
        return render(request, 'user.html', {'users': users})


def create_user(request):
    # usernames = User.objects.all().values_list('username', flat=True)
    # print(usernames)
    return render(request, 'create_user.html')


def validate_user(request):
    username = request.POST['username']
    email = request.POST['email']
    pass1 = request.POST['password1']
    pass2 = request.POST['password2']

    form = (
        ('email', email)
    )

    return render(request, 'thanks.html', {'form': form})


def username_exists(username):
    return User.objects.filter(username=username).exists()


def email_exists(email):
    return User.objects.filter(email=email).exists()
