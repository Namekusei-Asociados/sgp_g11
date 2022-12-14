from django.urls import path

from accounts import views

urlpatterns = [
    # Home page
    path('', views.home, name='base'),
    path('home/', views.home, name='home'),
    path('index_user',views.index,name='accounts.index'),
    path('create_user/', views.create_user, name='accounts.create_user'),
    path('edit_user/', views.edit_user, name='accounts.edit_user'),
    path('validate_user/', views.validate_user, name='accounts.validate_user'),

    path('edit_user/<str:username>/', views.edit_user, name='accounts.edit_user'),
    path('validate_edit_user/', views.validate_edit_user, name='accounts.validate_edit_user'),
    path('delete/<str:username>', views.destroy, name='accounts.delete')
]
