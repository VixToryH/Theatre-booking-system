from django.db import models #модель профілю користувача
from django.conf import settings #зв’язок 1 до 1 з таблицею користувачів

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, #використовує стандартну або кастомну модель User
        on_delete=models.CASCADE,
        related_name='profile' #доступ до профілю через user.profile
    )
    phone = models.CharField(
        max_length=20
    )
    preferred_performance_type = models.CharField(
        max_length=50,
        choices=[
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
        ],
        blank=True, null=True #поле не обов’язкове
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): #текстове представлення об’єкта
        return f"{self.user.username} profile"
