from django.urls import path

from user_story import views

urlpatterns = [
    # Path for user_story
    path('backlog/', views.backlog, name='user_story.backlog'),
    path('create_user_story/', views.create_user_story, name='user_story.create_user_story'),
    path('validate_create_user_story/', views.validate_create_user_story, name='user_story.validate_create_user_story'),
    path('edit_user_story/<int:id_user_story>', views.edit_user_story, name='user_story.edit_user_story'),
    path('history/<int:id_user_story>', views.history, name='user_story.history'),
    path('validate_edit_user_story/', views.validate_edit_user_story, name='user_story.validate_edit_user_story'),
    path('cancel_user_story/<int:id_user_story>', views.cancel_user_story, name='user_story.cancel_user_story'),
    path('validate_cancel_user_story/', views.validate_cancel_user_story, name='user_story.validate_cancel_user_story'),
    path('details_user_story/<int:id_user_story>', views.details_user_story, name='user_story.details_user_story'),
    path('details_user_story/<int:id_user_story>/attachment/<int:id_attachment>', views.download_us_attachment,name='user_story.download_us_attachment'),
]
