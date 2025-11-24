from rest_framework import serializers
from .models import Show, Genre, Seat

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # показує жанри як список об’єктів

    class Meta:
        model = Show
        fields = [
            'id',
            'title',
            'description',
            'date',
            'time',
            'status',
            'genres',
            'duration',
            'hall',
            'price'
        ]

class SeatSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'is_vip', 'is_available']

    def get_is_available(self, seat):
        show_id = self.context.get("show_id")
        if not show_id:
            return True

        from bookings.models import Booking
        return not Booking.objects.filter(
            show_id=show_id,
            seat=seat,
            status='confirmed'
        ).exists()

