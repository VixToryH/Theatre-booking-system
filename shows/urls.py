from django.urls import path
from .views import (
    ShowListView,
    ShowDetailView,
    seats_for_show,
    cancel_show,
)

urlpatterns = [
    path("", ShowListView.as_view(), name="show-list"),
    path("<int:pk>/", ShowDetailView.as_view(), name="show-detail"),
    path("<int:pk>/seats/", seats_for_show, name="show-seats"),
    path("<int:pk>/cancel/", cancel_show),
]
