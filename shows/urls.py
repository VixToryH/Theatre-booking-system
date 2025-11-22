from django.urls import path
from .views import (
    ShowListView,
    ShowDetailView,
    cancel_show,
)

urlpatterns = [
    # API routes
    path("api/", ShowListView.as_view(), name="show-list"),
    path("api/<int:pk>/", ShowDetailView.as_view(), name="show-detail"),
    path("<int:pk>/cancel/", cancel_show),
]
