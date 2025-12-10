from django.db import models, transaction, IntegrityError
from django.conf import settings
from shows.models import Show, Seat


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT
    )

    price_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'seat'],
                name='unique_booking_for_show_seat'
            )
        ]

    def __str__(self):
        if self.seat_id:
            try:
                seat_info = f"row {self.seat.row}, seat {self.seat.number}"
            except Exception:
                seat_info = "invalid seat"
        else:
            seat_info = "no seat (view)"

        return f"{self.user.username} - {self.show.title} - {seat_info}"

    @classmethod
    def create_booking_safe(cls, user, show, seat, price=None):
        try:
            with transaction.atomic():

                base_price = show.price
                vip_extra = 200 if seat and seat.is_vip else 0
                total_price = base_price + vip_extra

                booking = cls.objects.create(
                    user=user,
                    show=show,
                    seat=seat,
                    price_paid=total_price,
                    status='confirmed'
                )

                return booking, True

        except IntegrityError:
            return None, False
