from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

class Theater(models.Model):
    name = models.CharField(max_length=150, default='Театр "Голос Емоцій"')
    address = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Seat(models.Model):
    row = models.IntegerField()
    number = models.IntegerField()
    is_vip = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['row', 'number'], name='unique_seat')
        ]

    def __str__(self):
        vip = " (VIP)" if self.is_vip else ""
        return f"Ряд {self.row}, Місце {self.number}{vip}"


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Show(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('cancelled', 'Скасована'),
        ('finished', 'Завершена'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    genres = models.ManyToManyField(Genre, related_name='shows', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  #коли виставу додали в базу
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.date} {self.time})"

    def is_finished(self):  # перевіряє, чи вистава вже минула
        dt = timezone.make_aware(datetime.combine(self.date, self.time))
        return timezone.now() > dt

    def cancel_show(self): #скасування вистави і розсилка листів
        self.is_cancelled = True
        self.save()

        # Імпортуємо тут, щоб уникнути циклічного імпорту
        from bookings.models import Booking

        bookings = Booking.objects.filter(show=self)

        for booking in bookings:
            user_email = booking.user.email
            send_mail(
                subject=f'Виставу "{self.title}" скасовано',
                message=(
                    f'Шановний(а) {booking.user.username},\n\n'
                    f'Повідомляємо, що вистава "{self.title}" '
                    f'яку Ви забронювали на {self.date.strftime("%d.%m.%Y %H:%M")}, була скасована.\n\n'
                    f'Оплату буде повернено найближчим часом.\n\n'
                    f'З повагою, Театр "Voice of Emotions".'
                ),
                from_email=None,
                recipient_list=[user_email],
                fail_silently=False,
            )


