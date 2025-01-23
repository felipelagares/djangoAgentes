import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_root.settings')
django.setup()

from genericApp.models import Film


def search(film_name) -> []:  # busca filmes semelhantes a partir de um nome
    # ------------------lendo um csv---------------------------

    # -------------------usando bdd----------------------------
    film = Film.objects.filter(name__contains=film_name)
    all_films = Film.objects.filter(genre__contains=film.genres)

    return list(all_films)


def pre_recommend():
    films = Film.objects.order_by('rating')[:10]
    return films


if __name__ == '__main__':

    # df = pd.read_csv(r'C:\Users\felip\Desktop\workspace\djangoAgentes\media\movies.csv')
    # for _, line in df.iterrows():
    #     Film.objects.get_or_create(
    #         id=line['movieId'],
    #         defaults={
    #             'name': line['title'],
    #             'genres': line['genres'],
    #         },
    #     )
    df = pd.read_csv(r'C:\Users\felip\Desktop\workspace\djangoAgentes\media\ratings.csv')
    for _, line in df.iterrows():
        film_id = line['movieId']  # Nome da coluna no CSV para o ID
        new_rating = line['rating']  # Nome da coluna no CSV para o rating
        Film.objects.filter(id=film_id).update(rating=new_rating)
