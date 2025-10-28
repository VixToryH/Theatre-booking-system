from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # GET - всім, POST/PUT/DELETE - лише авторизованим

    def perform_create(self, serializer):
        #прив’язування бронювання до конкретного користувача
        serializer.save(user=self.request.user)
