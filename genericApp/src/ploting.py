import base64

import matplotlib.pyplot as plt
import io
import urllib
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def plot_film_ratings(filmes):
    ratings = [film.rating for film in filmes]
    film_names = [film.name for film in filmes]

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(film_names, ratings, color='skyblue')

    # Adicionando rótulos e título
    ax.set_xlabel('Filmes')
    ax.set_ylabel('Avaliação')
    ax.set_title('Avaliação dos Filmes')

    # Rotacionando os nomes dos filmes no eixo X para ficarem legíveis
    plt.xticks(rotation=45, ha="right")

    # Salvar o gráfico em um objeto BytesIO para ser retornado como uma imagem
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Codificando a imagem em base64 para ser usada no HTML
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    buf.close()  # Fechar o buffer de memória

    return img_data

    return img_data
