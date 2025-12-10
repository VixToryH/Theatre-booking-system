from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import (
    BookingModelSerializer,
    BookingCreateSerializer,
    BookingListSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookingModelSerializer
        return BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        created = result.get("bookings", [])
        failed = result.get("failed", [])

        if len(created) == 0:
            return Response(
                {"detail": "Не вдалося створити жодного бронювання.", "failed": failed},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(result, status=status.HTTP_201_CREATED)

    # Новий кастомний action для "моїх бронювань"
    @action(detail=False, methods=["get"], url_path="my")
    def my_bookings(self, request):
        bookings = (
            Booking.objects
            .filter(user=request.user)
            .select_related("show", "seat")
        )
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
