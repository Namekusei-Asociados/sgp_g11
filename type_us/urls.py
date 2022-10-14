from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='type_us.index'),
    path('', views.create, name='type_us.create'),
    # path('edit/<int:id>', views.edit, name='projects.edit'),
    path('store', views.store, name='type_us.store'),
    # path('update', views.update, name='projects.update')
    #importacion de roles de otros proyectos
    path('import', views.import_type_us, name='type_us.import_type_us')
]
