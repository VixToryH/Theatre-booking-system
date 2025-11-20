from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shows.models import Show
from .recommender import Recommender
from shows.serializers import ShowSerializer

recommender = Recommender()

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        recommender.load_data()
        recommender.train_cf()
        recommender.train_cbf()

        recommended_ids = recommender.get_recommendations_for_user(user.id)

        shows = Show.objects.filter(id__in=recommended_ids)
        serialized = ShowSerializer(shows, many=True)

        return Response({
            "user": user.id,
            "recommendations": serialized.data
        })


class SimilarShowsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, show_id):
        recommender.load_data()
        recommender.train_cf()
        recommender.train_cbf()

        similar_ids = recommender.get_similar_shows(show_id)

        shows = Show.objects.filter(id__in=similar_ids)
        serialized = ShowSerializer(shows, many=True)

        return Response({
            "base_show": show_id,
            "similar": serialized.data
        })
