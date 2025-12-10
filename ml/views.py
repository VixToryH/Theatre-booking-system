from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shows.models import Show
from .recommender import Recommender
from shows.serializers import ShowSerializer
from .models import Rating
from .serializers import RatingSerializer

recommender = Recommender()


class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        recommender.load_data()
        recommender.train_cf()
        recommender.train_cbf()

        recommended_ids = recommender.get_recommendations_for_user(user.id)

        if not recommended_ids:
            try:
                recommended_ids = recommender.get_top_shows_by_content(limit=10)
            except:
                recommended_ids = []

        if not recommended_ids:
            recommended_ids = list(
                Show.objects.values_list('id', flat=True)[:10]
            )

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

        if not similar_ids:
            try:
                similar_ids = recommender.get_top_shows_by_content(limit=5)
            except:
                similar_ids = list(Show.objects.values_list('id', flat=True)[:5])

        shows = Show.objects.filter(id__in=similar_ids)
        serialized = ShowSerializer(shows, many=True)

        return Response({
            "base_show": show_id,
            "similar": serialized.data
        })


class RatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        show_id = request.data.get("show_id")
        rating_value = request.data.get("rating")

        if show_id is None or rating_value is None:
            return Response({"error": "show_id and rating required"}, status=400)

        try:
            show = Show.objects.get(id=show_id)
        except Show.DoesNotExist:
            return Response({"error": "Show not found"}, status=404)

        rating, created = Rating.objects.update_or_create(
            user=user,
            show=show,
            defaults={"rating": rating_value}
        )

        return Response({
            "message": "Rating saved",
            "created": created,
            "rating": RatingSerializer(rating).data
        })

    def get(self, request, show_id):
        user = request.user
        try:
            rating = Rating.objects.get(user=user, show_id=show_id)
            return Response(RatingSerializer(rating).data)
        except Rating.DoesNotExist:
            return Response({"rating": 0})
