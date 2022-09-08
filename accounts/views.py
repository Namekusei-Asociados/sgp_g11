from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User


# Create your views here.
@login_required()
def home(request):
    user = request.user
    if user.role_sys == 'admin':
        users = User.objects.all()
        return render(request, 'dashboard/admin.html', {'users': users})

    elif user.role_sys == 'user':
        return render(request, 'dashboard/user.html')
    else:
        return render(request, 'dashboard/visitor.html')


@login_required()
def admin_index(request):
    users = User.objects.all()
    return render(request, 'account/index.html', {'users': users})
