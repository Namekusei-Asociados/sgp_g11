from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="sprints.index"),
    path('create_sprint/', views.create_sprint, name="sprints.create_sprint"),
    path('validate_create_sprint/', views.validate_create_sprint, name="sprints.validate_create_sprint"),
    path('edit_sprint/', views.edit_sprint, name="sprints.edit_sprint"),
    path('validate_edit_sprint/', views.validate_edit_sprint, name="sprints.validate_edit_sprint"),
    path('cancel_sprint/', views.cancel_sprint, name="sprints.cancel_sprint"),
    path('validate_cancel_sprint/', views.validate_cancel_sprint, name="sprints.validate_cancel_sprint"),
]
