from django.urls import path
from . import views

urlpatterns = [
    # path('index', views.index, name='projects.index'),
    path('', views.create, name='type_us.create'),
    # path('edit/<int:id>', views.edit, name='projects.edit'),
    # path('store', views.store, name='projects.store'),
    # path('update', views.update, name='projects.update')
]
