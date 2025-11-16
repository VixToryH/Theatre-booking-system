from django.db import models
from django.conf import settings

class PerformanceType(models.Model):
    GENRE_CHOICES = [
        ('tragedy', 'Трагедія'),
        ('comedy', 'Комедія'),
        ('farce', 'Фарс'),
        ('satire', 'Сатира'),
        ('mystery', 'Містерія'),
        ('historical', 'Історична вистава'),
        ('opera', 'Опера'),
        ('operetta', 'Оперета'),
        ('ballet', 'Балетна вистава'),
        ('circus', 'Циркова вистава'),
        ('monoplay', 'Вистава одного актора'),
        ('children', 'Дитяча вистава'),
    ]

    code = models.CharField(max_length=50, choices=GENRE_CHOICES, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20)

    preferred_performance_types = models.ManyToManyField(
        PerformanceType,
        blank=True,
        related_name='users'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"
