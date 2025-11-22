from django.urls import path
from .views import RecommendationView, SimilarShowsView

urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('recommendations/similar/<int:show_id>/', SimilarShowsView.as_view(), name='similar_shows'),
]

