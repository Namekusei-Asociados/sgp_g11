from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="sprints.index"),
    path('create_sprint/', views.create_sprint, name="sprints.create_sprint"),
    path('validate_create_sprint/', views.validate_create_sprint, name="sprints.validate_create_sprint"),
]
