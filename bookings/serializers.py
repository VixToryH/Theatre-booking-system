from rest_framework import serializers
from .models import Booking
from shows.models import Show, Seat
from django.db import transaction, IntegrityError


class BookingModelSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = ('id', 'show', 'seat', 'price_paid', 'status', 'created_at', 'user')


class BookingCreateSerializer(serializers.Serializer):
    show = serializers.PrimaryKeyRelatedField(queryset=Show.objects.all())
    seats = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    bookings = serializers.ListField(read_only=True)
    failed = serializers.ListField(read_only=True)

    def validate(self, data):
        show = data["show"]
        seat_ids = data["seats"]

        seats_qs = Seat.objects.filter(id__in=seat_ids)
        if seats_qs.count() != len(seat_ids):
            raise serializers.ValidationError("Одне або декілька місць не існують.")

        occupied = []
        for seat in seats_qs:
            if Booking.objects.filter(show=show, seat=seat).exists():
                occupied.append(f"{seat.row}.{seat.number}")
        if occupied:
            raise serializers.ValidationError(f"Наступні місця вже заброньовані: {', '.join(occupied)}")

        data["seats_objects"] = list(seats_qs)
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        show = validated_data["show"]
        seats = validated_data["seats_objects"]

        created = []
        failed = []

        for seat in seats:
            try:
                booking, ok = Booking.create_booking_safe(user=user, show=show, seat=seat)
                if ok and booking:
                    created.append({
                        "id": booking.id,
                        "show": booking.show.id,
                        "seat": booking.seat.id if booking.seat else None,
                        "row": booking.seat.row if booking.seat else None,
                        "number": booking.seat.number if booking.seat else None,
                        "price_paid": str(booking.price_paid) if booking.price_paid is not None else None,
                        "created_at": booking.created_at,
                    })
                else:
                    failed.append({"seat_id": seat.id, "reason": "Integrity error or already booked"})
            except IntegrityError:
                failed.append({"seat_id": seat.id, "reason": "IntegrityError"})
            except Exception as e:
                failed.append({"seat_id": seat.id, "reason": str(e)})

        return {"bookings": created, "failed": failed}
