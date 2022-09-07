from django.urls import path

from accounts import views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('validate_user/', views.validate_user, name='validate_user'),
]
