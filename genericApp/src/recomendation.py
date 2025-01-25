import ast

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import django
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# settando o django para poder usar os models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_root.settings')
django.setup()

from genericApp.models import Film

# escolhendo um modelo de llm para processamento de texto em inglês (sugestão de modelo do gpt)
model = SentenceTransformer('all-MiniLM-L6-v2')
filmes = Film.objects.all()


# gera a vetorizaçao das descriçoes pre-processadas e as processa caso ja nao estejam.
# pré-processar significa a remoçao de caracteres especiais e stop words do texto
def precalculate_embeddings(filmes):
    embeddings = {}
    for film in filmes:
        preprocessed_text = film.clean_desc
        if not preprocessed_text:
            preprocessed_text = preprocess_text(film.description)
            film.clean_desc = preprocessed_text
            film.save()
        embeddings[film.id] = model.encode(preprocessed_text)
    return embeddings


# carregar os embeddings sempre que o servidor for iniciar. carregá-los a cada requisiçao teria um custo gigantesco
# de tempo por isso é calculado a partir do banco de dados antes de iniciar o serviço. Quabt maior o Banco de dados
# mais tempo será gasto nesses cálculos. O meu tem 2800 filmes (isso é teoricamente pouco) e demora alguns segundos
film_embeddings = precalculate_embeddings(filmes)


# pre-processamento das palavras na descriçao do filme
def preprocess_text(text):
    # Converter para minúsculas
    text = text.lower()
    # Remover números e pontuações, exceto vírgulas
    text = re.sub(r'[^\w\s,]', '', text)
    text = re.sub(r'\d+', '', text)
    # Tokenização
    tokens = word_tokenize(text)
    # Remover stopwords
    stop_words = set(stopwords.words('english'))

    # token recebe uma lista onde cada elemento é:
    # um token para cada token na lista de tokens passada caso o token nao seja um 'stop_word'
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)


# calcula a similaridade semantica entre os filmes, não possui um longo tempo de espera pois os objetos comparados foram
# vetorizados ao calcular os embeddings
def calculate_semantic_similarity(embedding_a, embedding_b):
    similarity = cosine_similarity([embedding_a], [embedding_b])[0][0]
    return similarity * 100


# obtém os 5 filmes mais similares, retorna uma lista de listas do tipo [id_do_filme, similaridade_com_o_filme_buscado]
# ou uma string caso o filme buscado não esteja no banco de dados
def get_recommendations(title):
    embeddings = film_embeddings
    searched_film = Film.objects.filter(name=title).first()
    if searched_film:
        searched_embedding = embeddings[searched_film.id]

        similares = []
        for film in filmes:
            current_embedding = embeddings[film.id]
            similarity = calculate_semantic_similarity(current_embedding, searched_embedding)
            similares.append([film.id, similarity])

        # Ordenar por similaridade decrescente
        similares.sort(key=lambda x: x[1], reverse=True)
        return similares[:5]
    else:
        return 'Film not found'


# O que estiver dentro deste if só será executado se este arquivo .py estiver sendo executado diretamente
# o python trabalha com threads ao interpretar os arquivos, esse é a principal funçao dessa main na minha opinião
if __name__ == '__main__':
    filmes = Film.objects.all()
    for filme in filmes:
        desc = filme.description
        clean_desc = preprocess_text(desc)
        filme.clean_desc = clean_desc
        filme.save()

    # df = pd.read_csv(r'C:\Users\felip\Desktop\workspace\djangoAgentes\media\movies_metadata.csv', low_memory=False)
    #
    # # Limpeza de dados
    # df['title'] = df['title'].fillna('No Title')
    # df['overview'] = df['overview'].fillna(pd.NA)  # Permite valores nulos para `description`
    # df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(pd.NA)  # Permite valores nulos
    # df['genres'] = df['genres'].fillna('[]')  # Garante que o campo `genres` sempre tenha um valor
    #
    # # Converte o campo `genres` para string legível
    # def parse_genres(genres):
    #     try:
    #         genres_list = ast.literal_eval(genres)  # Converte string para lista de dicionários
    #         return ', '.join([g['name'] for g in genres_list])
    #     except (ValueError, TypeError):
    #         return None  # Retorna None para valores inválidos
    #
    #
    # df['genres'] = df['genres'].apply(parse_genres)
    #
    # df = df.drop_duplicates(subset='id', keep='first')  # Mantém a primeira ocorrência de cada ID
    #
    # # Inserir os dados na tabela Film
    # for row in df.iterrows():
    #     name = row[1]['title']
    #     description = row[1]['overview']
    #     rating = row[1]['vote_average']
    #     genres = row[1]['genres']
    #     film_id = row[1]['id']
    #
    #     # Verifique se o ID já existe na tabela antes de inserir
    #     if not Film.objects.filter(id=film_id).exists():
    #         Film.objects.create(id=film_id, name=name, description=description, rating=rating, genres=genres)
    #     else:
    #         print(f"ID {film_id} já existe. Pular inserção.")
