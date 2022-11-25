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
    path('init_sprint/<int:id_sprint>', views.init_sprint, name="sprints.init_sprint"),

    # View sprint
    path('<int:id_sprint>/dashboard', views.dashboard, name='sprints.dashboard'),

    # Members
    path('<int:id_sprint>/members', views.members, name='sprints.members.index'),
    path('<int:id_sprint>/members/add', views.add_member, name='sprints.members.add'),
    path('<int:id_sprint>/members/edit/<int:member_id>', views.edit_member, name='sprints.members.edit'),
    path('<int:id_sprint>/members/update', views.update_member, name='sprints.members.update'),
    path('<int:id_sprint>/members/store', views.store_member, name='sprints.members.store'),
    path('<int:id_sprint>/members/destroy/<int:member_id>', views.delete_member, name='sprints.members.delete'),
    path('<int:id_sprint>/members/change/<int:member_id>', views.change_member, name='sprints.members.change'),
    path('<int:id_sprint>/members/validate_change', views.validate_change_member,
         name='sprints.members.validate.change'),

    # Sprint backlog
    path('<int:id_sprint>/sprint_bakclog', views.sprint_backlog, name='sprints.sprint_backlog.index'),
    path('<int:id_sprint>/sprint_bakclog/add', views.add_sprint_backlog, name='sprints.sprint_backlog.add'),
    path('<int:id_sprint>/sprint_bakclog/store', views.store_sprint_backlog, name='sprints.sprint_backlog.store'),
    path('<int:id_sprint>/sprint_backlog/details/<int:id_user_story>', views.details_sprint_backlog,
         name='sprints.sprint_backlog.details'),
    path('<int:id_sprint>/sprint_backlog/edit/<int:id_user_story>', views.edit_sprint_backlog,
         name='sprints.sprint_backlog.edit'),
    path('<int:id_sprint>/sprint_bakclog/update', views.update_sprint_backlog, name='sprints.sprint_backlog.update'),
    path('<int:id_sprint>/sprint_backlog/destroy', views.delete_sprint_backlog, name='sprints.sprint_backlog.delete'),

    # Kanban
    path('<int:id_sprint>/kanban', views.kanban_index, name='sprints.kanban.index'),
    path('<int:id_sprint>/user_story/status', views.kanban_user_story_change_status,
         name='sprints.kanban.user_story.change_status_kanban'),
    path('<int:id_sprint>/user_story/task/store', views.kanban_task_store, name='sprints.kanban.user_story.task_store'),
    path('<int:id_sprint>/user_story/task/finished', views.kanban_task_finished,
         name='sprints.kanban.user_story.task_finished'),

    # Burn down chart
    path('<int:id_sprint>/burndown_chart', views.burndown_chart, name='sprints.burndown_chart'),

    # US review
    path('<int:id_sprint>/us_review', views.us_review, name='sprints.us_review'),
    path('<int:id_sprint>/us_review/confirm', views.us_review_confirm, name='sprints.us_review.confirm'),
    path('<int:id_sprint>/us_review/reject', views.us_review_reject, name='sprints.us_review.reject')

]
