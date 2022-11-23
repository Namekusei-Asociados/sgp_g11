from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='meetings.index'),
    path('details/<int:id>', views.details, name='meetings.details'),
    path('create', views.create, name='meetings.create'),
    path('edit/<int:id>', views.edit, name='meetings.edit'),
    path('store', views.store, name='meetings.store'),
    path('update/<int:id>', views.update, name='meetings.update'),
    path('delete/<int:id>', views.destroy, name='meetings.delete'),
]
