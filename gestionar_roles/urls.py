from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='gestionar_roles.index'),
    path('create', views.create, name='gestionar_roles.create'),
    path('store', views.store, name='gestionar_roles.store'),
    path('edit/<int:id>', views.edit, name='gestionar_roles.edit'),
    path('update', views.update, name='gestionar_roles.update')
]