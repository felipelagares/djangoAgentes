import ast
import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_root.settings')
django.setup()

from genericApp.models import Film

def populate(data):
    df = pd.read_csv(data)

    # Limpeza de dados
    df['title'] = df['title'].fillna('No Title')
    df['overview'] = df['overview'].fillna(pd.NA)  # Permite valores nulos para `description`
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(pd.NA)  # Permite valores nulos
    df['genres'] = df['genres'].fillna('[]')  # Garante que o campo `genres` sempre tenha um valor

    # Converte o campo `genres` para string legível
    def parse_genres(genres):
        try:
            genres_list = ast.literal_eval(genres)  # Converte string para lista de dicionários
            return ', '.join([g['name'] for g in genres_list])
        except (ValueError, TypeError):
            return None  # Retorna None para valores inválidos


    df['genres'] = df['genres'].apply(parse_genres)

    df = df.drop_duplicates(subset='id', keep='first')  # Mantém a primeira ocorrência de cada ID

    # Inserir os dados na tabela Film
    for row in df.iterrows():
        name = row[1]['title']
        description = row[1]['overview']
        rating = row[1]['vote_average']
        genres = row[1]['genres']
        film_id = row[1]['id']

        # Verifique se o ID já existe na tabela antes de inserir
        if not Film.objects.filter(id=film_id).exists():
            Film.objects.create(id=film_id, name=name, description=description, rating=rating, genres=genres)
        else:
            print(f"ID {film_id} já existe. Pular inserção.")
