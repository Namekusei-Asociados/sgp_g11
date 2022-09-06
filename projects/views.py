from django.shortcuts import render, redirect
from .models import Project
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request,'index.html')
