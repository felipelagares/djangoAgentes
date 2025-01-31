from rest_framework import serializers
from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film  # informar qual classe quero transformar em json
        fields = ['id', 'name', 'description', 'rating', 'genres']  # informar quais campos quero transformar em json
