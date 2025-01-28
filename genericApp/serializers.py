from rest_framework import serializers
from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film  # informar qual classe quero transformar em json
        fields = '__all__'  # informar quais campos da classe quero transformar em json
