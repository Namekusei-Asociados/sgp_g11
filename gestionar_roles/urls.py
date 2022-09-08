from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='gestionar_roles.create'),
    #path('store', views.store, name='projects.store')
]
