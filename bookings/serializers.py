from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        """
        Перевірки перед створенням бронювання.
        """
        show = data['show']
        seat = data['seat']

        # 🔹 Перевіряємо, чи місце вже заброньоване на цей сеанс
        if Booking.objects.filter(show=show, seat=seat).exists():
            raise serializers.ValidationError("Це місце вже заброньоване для цього сеансу.")

        # 🔹 Перевірка наявності вільних місць (якщо у моделі Show є available_seats)
        if hasattr(show, 'available_seats') and show.available_seats <= 0:
            raise serializers.ValidationError("Немає вільних місць для цього сеансу.")

        # 🔹 Опціонально: перевіряємо ціну
        if 'price_paid' in data and hasattr(seat, 'price'):
            if data['price_paid'] < seat.price:
                raise serializers.ValidationError("Сплачена сума менша за ціну місця.")

        return data

    def create(self, validated_data):
        """
        Створення бронювання — автоматично додає користувача.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        booking = Booking.objects.create(**validated_data)
        return booking
