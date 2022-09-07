from django.urls import path
from . import views

urlpatterns = [
    path('', views.create, name='projects.create'),
    path('store', views.store, name='projects.store')
]
