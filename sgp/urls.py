"""sgp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Examples:
Function views

    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Index page
    path('', TemplateView.as_view(template_name="account/base.html")),

    # Projects urls
    path('projects/', include('projects.urls')),

    # Super-admin page
    path('admin/', admin.site.urls),

    # Home page
    path('home/', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),

    # Visitor page
    path('visitor/', TemplateView.as_view(template_name='dashboard/visitor.html'), name='visitor'),

    # Register OAuth URLs
    path('accounts/', include('allauth.urls')),
]