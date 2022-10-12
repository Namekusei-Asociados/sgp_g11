from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="sprints.index"),
    path('create_sprint/', views.create_sprint, name="sprints.create_sprint"),
    path('validate_create_sprint/', views.validate_create_sprint, name="sprints.validate_create_sprint"),
    path('edit_sprint/<int:id_sprint>', views.edit_sprint, name="sprints.edit_sprint"),
    path('validate_edit_sprint/', views.validate_edit_sprint, name="sprints.validate_edit_sprint"),
    path('cancel_sprint/<int:id_sprint>', views.cancel_sprint, name="sprints.cancel_sprint"),
    path('validate_cancel_sprint/', views.validate_cancel_sprint, name="sprints.validate_cancel_sprint"),

    # View sprint
    path('<int:id_sprint>/', views.sprint, name="sprints.sprint"),

    # Members
    path('<int:id_sprint>/members', views.members, name='sprints.members.index'),
    path('<int:id_sprint>/members/create', views.create_member, name='sprints.members.create'),
    path('<int:id_sprint>/members/edit/<int:member_id>', views.edit_member, name='sprints.members.edit'),
    path('<int:id_sprint>/members/update', views.update_member, name='sprints.members.update'),
    path('<int:id_sprint>/members/store', views.store_member, name='sprints.members.store'),
    path('<int:id_sprint>/members/destroy/<int:member_id>', views.delete_member, name='sprints.members.delete'),
]
