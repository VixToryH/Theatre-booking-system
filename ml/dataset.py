import random
from django.contrib.auth.models import User
from shows.models import Show
from bookings.models import Booking

def generate_ml_dataset():
    """
    rating = 4-5 якщо було бронювання
    rating = 1-3 якщо це випадковий перегляд
    """
    data = []

    bookings = Booking.objects.all()
    for b in bookings:
        data.append({
            "user_id": b.user.id,
            "show_id": b.show.id,
            "rating": random.choice([4, 5])
        })

    all_users = User.objects.all()
    all_shows = list(Show.objects.all())

    for user in all_users:
        print("SHOWS COUNT:", len(all_shows))
        print("SHOWS:", all_shows)

        max_k = min(len(all_shows), 6)
        watched = random.sample(all_shows, k=random.randint(2, max_k))

        for show in watched:
            if not Booking.objects.filter(user=user, show=show).exists():
                data.append({
                    "user_id": user.id,
                    "show_id": show.id,
                    "rating": random.choice([1, 2, 3])
                })

    return data
