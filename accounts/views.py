from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):
    if request.user.role_sys == 'visitor':
        return render(request, 'dashboard/visitor.html')
    else:
        return render(request, 'dashboard/home.html')
