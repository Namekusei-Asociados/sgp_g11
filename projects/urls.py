from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.index, name='projects.index'),
    path('', views.create, name='projects.create'),
    path('edit/<int:id>', views.edit, name='projects.edit'),
    path('store', views.store, name='projects.store'),
    path('update', views.update, name='projects.update'),

    path('<int:id_project>', views.dashboard, name='projects.dashboard'),

    # Users Story urls
    path('<int:id_project>/user_story/', include('user_story.urls')),

    # Type Users Stories urls
    path('<int:id_project>/type-us/', include('type_us.urls')),

    # Sprint urls
    path('<int:id_project>/sprint/', include('sprints.urls'))
]
