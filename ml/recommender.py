import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from shows.models import Show
from bookings.models import Booking

class Recommender:

    def __init__(self):
        self.ratings_matrix = None
        self.item_similarity = None
        self.genre_sim = None

    def load_data(self):
        bookings = Booking.objects.all()

        data = []
        for b in bookings:
            data.append({
                "user_id": b.user.id,
                "show_id": b.show.id,
                "rating": 5,
            })

        df = pd.DataFrame(data)
        if df.empty:
            return False

        self.ratings_matrix = df.pivot_table(
            index="user_id",
            columns="show_id",
            values="rating"
        ).fillna(0)
        return True


    def train_cf(self):
        if self.ratings_matrix is None:
            return False

        sim = cosine_similarity(self.ratings_matrix.T)
        self.item_similarity = pd.DataFrame(
            sim,
            index=self.ratings_matrix.columns,
            columns=self.ratings_matrix.columns
        )
        return True


    def get_cf_recommendations(self, user_id, top_n=5):
        if user_id not in self.ratings_matrix.index:
            return []

        user_ratings = self.ratings_matrix.loc[user_id]
        watched = user_ratings[user_ratings > 0].index

        scores = self.item_similarity.loc[watched].sum().sort_values(ascending=False)
        scores = scores.drop(watched, errors="ignore")

        return list(scores.head(top_n).index)


    def train_cbf(self):
        shows = list(Show.objects.all())

        if not shows:
            return False

        genres_text = [" ".join(g.name for g in s.genres.all()) for s in shows]

        vect = TfidfVectorizer()
        tfidf = vect.fit_transform(genres_text)

        sim = cosine_similarity(tfidf)
        self.genre_sim = pd.DataFrame(
            sim,
            index=[s.id for s in shows],
            columns=[s.id for s in shows]
        )
        return True


    def get_similar_by_genre(self, show_id, top_n=5):
        if self.genre_sim is None or show_id not in self.genre_sim.index:
            return []

        scores = self.genre_sim.loc[show_id].sort_values(ascending=False)
        scores = scores.drop(show_id, errors="ignore")
        return list(scores.head(top_n).index)


    def hybrid_recommendations(self, user_id, top_n=5, w_cf=0.5, w_cbf=0.5):
        cf_rec = self.get_cf_recommendations(user_id, top_n=20)

        cbf_scores = {}
        for sid in cf_rec:
            if sid not in self.genre_sim.index:
                continue

            similar = self.genre_sim.loc[sid]
            for s2, score in similar.items():
                cbf_scores[s2] = cbf_scores.get(s2, 0) + score * w_cbf

        cf_scores = {sid: (i * w_cf) for i, sid in enumerate(cf_rec[::-1])}

        combined = {}
        for sid in set(cf_scores) | set(cbf_scores):
            combined[sid] = cf_scores.get(sid, 0) + cbf_scores.get(sid, 0)

        final_sorted = sorted(combined.items(), key=lambda x: x[1], reverse=True)

        return [sid for sid, _ in final_sorted[:top_n]]
