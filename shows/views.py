from rest_framework import generics, permissions
from .models import Show
from .serializers import ShowSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ml.recommender import Recommender
from django.shortcuts import render, get_object_or_404
from .models import Seat
from .serializers import SeatSerializer

recommender = Recommender()

@api_view(['POST'])
def cancel_show(request, pk):
    try:
        show = Show.objects.get(pk=pk)
        show.cancel_show()
        return Response({'message': 'Виставу скасовано та повідомлення надіслані.'})
    except Show.DoesNotExist:
        return Response({'error': 'Виставу не знайдено.'}, status=404)


class ShowListView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class UserRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        recommender.load_data()
        recommender.train_cf()
        recommender.train_cbf()

        recs = recommender.hybrid_recommendations(user.id)
        return Response({"recommendations": recs})


class SimilarShowsView(APIView):
    def get(self, request, show_id):

        recommender.load_data()
        recommender.train_cbf()

        similar = recommender.get_similar_by_genre(show_id)
        return Response({"similar": similar})

@api_view(['GET'])
def seats_for_show(request, pk):
    show = get_object_or_404(Show, pk=pk)
    seats = Seat.objects.filter(hall=show.hall).order_by('row', 'number')

    serializer = SeatSerializer(
        seats,
        many=True,
        context={"show_id": pk}
    )
    return Response(serializer.data)


