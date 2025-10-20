"""
URL configuration for kursova project.

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shows.api_urls')),
]

from django.contrib import admin
from django.urls import path, include


