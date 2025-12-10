from rest_framework import routers
from django.urls import path, include
from .views import BookingViewSet

router = routers.DefaultRouter()
router.register(r'', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
