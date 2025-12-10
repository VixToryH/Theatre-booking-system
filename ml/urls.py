from django.urls import path
from .views import RecommendationView, SimilarShowsView, RatingView

urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('recommendations/similar/<int:show_id>/', SimilarShowsView.as_view(), name='similar_shows'),
    path('rate/', RatingView.as_view(), name='rate_show'),
    path('rate/<int:show_id>/', RatingView.as_view(), name='get_rating'),

]

