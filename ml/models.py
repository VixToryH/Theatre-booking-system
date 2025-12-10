from django.db import models
from django.contrib.auth.models import User
from shows.models import Show

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'show')

    def __str__(self):
        return f"{self.user.username} → {self.show.title}: {self.rating}"
