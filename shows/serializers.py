from rest_framework import serializers
from .models import Show, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # показує жанри як список об’єктів

    class Meta:
        model = Show
        fields = ['id', 'title', 'genres']
