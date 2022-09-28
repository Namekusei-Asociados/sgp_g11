from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.index, name='projects.index'),
    path('create', views.create, name='projects.create'),
    path('edit/<int:id_project>', views.edit, name='projects.edit'),
    path('store', views.store, name='projects.store'),
    path('update', views.update, name='projects.update'),
    path('cancel/<int:id_project>', views.cancel, name='projects.cancel'),


    path('<int:id_project>', views.dashboard, name='projects.dashboard'),
    path('<int:id_project>/members', views.members, name='projects.members.index'),
    path('<int:id_project>/members/create', views.create_member, name='projects.members.create'),
    path('<int:id_project>/members/edit/<int:member_id>', views.edit_member, name='projects.members.edit'),
    path('<int:id_project>/members/update/<int:member_id>', views.update_member, name='projects.members.update'),
    path('<int:id_project>/members/store', views.store_member, name='projects.members.store'),
    # Roles
    path('<int:id_project>/role/create', views.create_role, name='projects.create_role'),
    path('<int:id_project>/role/store', views.store_role, name='projects.store_role'),
    path('<int:id_project>/role/index', views.index_role, name='projects.index_role'),
    path('<int:id_project>/role/edit/<int:id>', views.edit_role, name='projects.edit_role'),
    path('<int:id_project>/role/update/<int:id>', views.update_role, name='projects.update_role'),
    path('<int:id_project>/role/delete/<int:id>', views.delete_role, name='projects.delete_role'),

    # Users Story urls
    path('<int:id_project>/user_story/', include('user_story.urls')),

    # Type Users Stories urls
    path('<int:id_project>/type-us/', include('type_us.urls')),

    # Sprint urls
    path('<int:id_project>/sprint/', include('sprints.urls'))
]
