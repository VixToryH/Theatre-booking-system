from django.urls import path
from .views import ShowListView, ShowDetailView, cancel_show

urlpatterns = [
    path("shows/", ShowListView.as_view(), name="show-list"),
    path("shows/<int:pk>/", ShowDetailView.as_view(), name="show-detail"),
    path('shows/<int:pk>/cancel/', cancel_show),
]
