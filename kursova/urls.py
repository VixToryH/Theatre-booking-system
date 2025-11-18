"""
URL configuration for kursova project.

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shows.views import UserRecommendationsView, SimilarShowsView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/', include('users.urls')),

    path('api/shows/', include('shows.urls')),

    path('api/bookings/', include('bookings.urls')),

    path("api/recommendations/", UserRecommendationsView.as_view()),
    path("api/recommendations/similar/<int:show_id>/", SimilarShowsView.as_view()),
]





