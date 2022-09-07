from django.urls import path

from accounts import views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
]
