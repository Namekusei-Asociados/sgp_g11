from django.urls import path

from accounts import views

urlpatterns = [
    # Home page
    path('home/', views.home, name='home'),
    path('create_user/', views.create_user, name='accounts.create_user'),
    path('validate_user/', views.validate_user, name='accounts.validate_user'),
]