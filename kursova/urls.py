"""
URL configuration for kursova project.

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shows.urls')),
    path('', include('bookings.urls')),
]




