from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.forms import SignupForm, UserForm, username_exists, email_exists
from accounts.models import User


@login_required()
def home(request):
    user = request.user
    if user.role_sys == 'admin':
        return render(request, 'dashboard/admin.html')
    elif user.role_sys == 'user':
        return render(request, 'dashboard/user.html')
    else:
        return render(request, 'dashboard/visitor.html')


def create_user(request):
    form = SignupForm()
    return render(request, 'user/create_user.html', {'form': form})


def validate_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        print(form)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if username_exists(username):
                return render(request, 'error.html', {'info': username})

            if email_exists(email):
                return render(request, 'error.html', {'info': email})

            if pass1 != pass2:
                return render(request, 'error.html', {'info': f'{pass1} | {pass2}'})

            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
        else:
            print('---------USERNAME ERROR--------------')
            return render(request, 'error.html', {'info': 'else isn\'n valid'})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'error.html', {'form': form})

