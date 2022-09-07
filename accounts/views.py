from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.forms import SignupForm, UserForm


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
        if form.is_valid():
            return render(request, 'thanks.html', {'info': request.POST['username']})
        else:
            print('---------USERNAME ERROR--------------')
            return render(request, 'error.html', {'info': 'else isn\'n valid'})

    # if a GET (or any other method) we'll create a blank form
    else:
        print('---------USERNAME ERROR--------------')
        return render(request, 'error.html', {'info': 'else reques method'})
