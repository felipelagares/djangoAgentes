import pandas as pd
from genericApp.models import Film


def search(film) -> []:
    all_films = Film.objects.filter(genre__contains=film.genres)


def pre_recommend():
    films = Film.objects.order_by('rating')[:10]
    return films[:10]
