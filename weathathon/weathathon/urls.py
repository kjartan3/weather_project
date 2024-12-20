"""
URL configuration for weathathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from weather_app.views import home_view, compare_view, save_view, search_view, handle_save_city, handle_delete_city

urlpatterns = [
    path('', home_view, name='home'),
    path('compare/', compare_view, name='compare'),
    path('save/', save_view, name='save'),
    path('save/city/', handle_save_city, name='handle_save_city'),
    path('delete/city/', handle_delete_city, name='handle_delete_city'),
    path('search/', search_view, name='search'),
    path('admin/', admin.site.urls),
    
]
