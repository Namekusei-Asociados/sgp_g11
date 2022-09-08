from django.urls import path

from accounts import views

urlpatterns = [
    # Home page
    path('home/', views.home, name='home'),
    path('create_user/', views.create_user, name='accounts.create_user'),
    path('user/', views.user, name='accounts.user'),
]
