from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='type_us.index'),
    path('', views.create, name='type_us.create'),
    path('edit/<int:id>', views.edit, name='type_us.edit'),
    path('store', views.store, name='type_us.store'),
    path('update/<int:id>', views.update, name='type_us.update'),
    path('delete/<int:id>', views.destroy, name='type_us.delete'),
    #importacion de roles de otros proyectos
    path('import', views.import_type_us, name='type_us.import_type_us')
]
