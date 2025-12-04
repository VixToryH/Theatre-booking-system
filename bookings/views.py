from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingModelSerializer, BookingCreateSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookingModelSerializer
        return BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        created = result.get("bookings", [])
        failed = result.get("failed", [])
        if len(created) == 0:
            return Response({"detail": "Не вдалося створити жодного бронювання.", "failed": failed},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)
