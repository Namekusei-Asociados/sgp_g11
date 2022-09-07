from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.forms import SignupForm


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
