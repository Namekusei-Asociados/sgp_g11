from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):
    user = request.user
    if user.role_sys == 'admin':
        return render(request, 'dashboard/admin.html')
    elif user.role_sys == 'user':
        return render(request, 'dashboard/user.html')
    else:
        return render(request, 'dashboard/visitor.html')
