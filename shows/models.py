from datetime import datetime
from django.db import models
from django.utils import timezone


class Theater(models.Model):
    name = models.CharField(max_length=150, default='Театр "Голос Емоцій"')
    address = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    number = models.IntegerField()
    is_vip = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hall', 'row', 'number'], name='unique_seat_in_hall')
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
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name="shows")

    def __str__(self):
        return f"{self.title} ({self.date} {self.time})"

    def is_finished(self):
        dt = timezone.make_aware(datetime.combine(self.date, self.time))
        return timezone.now() > dt
