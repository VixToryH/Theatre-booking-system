from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = ('id', 'show', 'seat', 'created_at', 'user')
        read_only_fields = ['created_at', 'user']

    def validate(self, data): #перевірка перед створенням
        show = data['show']
        seat = data['seat']

        if Booking.objects.filter(show=show, seat=seat).exists():
            raise serializers.ValidationError("Це місце вже заброньоване для цього сеансу.")

        if hasattr(show, 'available_seats') and show.available_seats <= 0:
            raise serializers.ValidationError("Немає вільних місць для цього сеансу.")

        if 'price_paid' in data and hasattr(seat, 'price'):
            if data['price_paid'] < seat.price:
                raise serializers.ValidationError("Сплачена сума менша за ціну місця.")

        return data

    def create(self, validated_data): #при створенні автоматично додаєтся користувач
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        booking = Booking.objects.create(**validated_data)
        return booking
