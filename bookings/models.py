from django.db import models, transaction, IntegrityError
from django.conf import settings
from shows.models import Show
from shows.models import Seat

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.PROTECT, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name='bookings')
    price_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['show', 'seat'], name='unique_booking_for_show_seat')
        ]

    def __str__(self):
        return f"{self.user} — {self.show} — {self.seat}"

    @classmethod
    def create_booking_safe(cls, user, show, seat, price=None):
        """
        Безпечне створення бронювання.
    Використовує транзакцію й ловить помилку, якщо місце вже зайняте.
        """
        try:
            with transaction.atomic(): #Атомарна транзакція—або все виконується, або нічого
                booking = cls.objects.create(
                    user=user,
                    show=show,
                    seat=seat,
                    price_paid=price or seat.price,
                    status='confirmed'
                )
                return booking, True
        except IntegrityError:
            # місце вже заброньоване на цей показ
            return None, False
