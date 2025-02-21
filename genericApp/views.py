import json

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import File, Film
from .serializers import FilmSerializer
from .src.populate import populate
from .src import recomendation, ploting, populate, analise
import urllib.parse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def file_upload_view(request):
    # view para receber um arquivo
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        uploaded_name = request.POST.get('name')
        if not uploaded_name:
            uploaded_name = uploaded_file.name

        if uploaded_file:
            populate(uploaded_file)
            File.objects.create(name=uploaded_name, file=uploaded_file)

        if request.POST['acao'] == 'populate':
            populate.populate(uploaded_file)

        return redirect('file_list')
    return render(request, 'file_upload.html')


def file_update_view(request, pk):
    # view para atualizar/deletar um arquivo
    file_instance = get_object_or_404(File, pk=pk)  # Obtém o registro

    if request.method == 'POST':
        if request.POST['acao'] == 'delete':
            file_instance.delete()
            return redirect('file_list')

        if request.POST['acao'] == 'update':
            file_instance.name = request.POST['name']
            file_instance.file = request.FILES['file']
            file_instance.save()
            return redirect('file_list')

    return render(request, 'file_update.html', {'file': file_instance})


def file_list_view(request):
    # view de listagem de arquivos
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})


def related_films_view(request):
    # view para a pagina de recomendaçao de filmes
    # no get ou primeiro acesso, renderizará a pagina normalmente
    if request.method == 'GET':
        return render(request, 'related_films.html', {'films': []})

    # no post, recebendo um nome de filme será buscado filmes semelhantes ao recebido se ele estiver na base de dados
    # ao encontrar os semelhantes gera um gráfico com os as avaliações
    if request.method == 'POST':
        film = request.POST['film']
        similaridades = recomendation.get_recommendations(title=film)
        if similaridades == 'Film not found':
            return render(request, 'related_films.html', {'films': []})
        relateds = []
        for item in similaridades:
            relateds.append(Film.objects.get(pk=item[0]))
            # ordenar por avaliação mais alta
            relateds.sort(key=lambda x: float(x.rating), reverse=True)
            img_data = ploting.plot_film_ratings(relateds)
        return render(request, 'related_films.html', {'films': relateds, 'img_data': img_data})


def film_details_view(request, pk):
    # view para visualizaçao de um filme
    film = Film.objects.get(pk=pk)
    return render(request, 'film_details.html', {'film': film})


class RecommendationViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Ao receber um nome de filme retorna os 5 filmes mais "
                              "parecidos com ele disponiveis na base de dados e um "
                              "grafico em base64 de suas avaliações",
        manual_parameters=[
            openapi.Parameter(
                name="film",
                in_=openapi.IN_QUERY,  # Especifica que o parâmetro está no link da requisição
                description="Nome do filme a ser buscado.",
                required=True,
                type=openapi.TYPE_STRING,
                default="Star Wars"
            ),
        ],
        responses={200: openapi.Response('Resposta de sucesso'),
                   400: openapi.Response('O parâmetro "film" é obrigatório'),
                   404: openapi.Response('Filme nao encontrado')
                   }
    )
    def recommend(self, request):
        film_name = request.GET.get('film', None)

        if not film_name:
            return Response({"error": "O parâmetro 'film' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar recomendações
        similaridades = recomendation.get_recommendations(title=film_name)

        if similaridades == 'Film not found':
            return Response({"error": "Filme não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Buscar os filmes recomendados
        relateds = [Film.objects.get(pk=item[0]) for item in similaridades]  # uma lista itens pega com os ids passados
        relateds.sort(key=lambda x: float(x.rating or 0), reverse=True)

        # ------------------ Usando serializers --------------------------------------------
        # Serializar os dados dos filmes
        serializer = FilmSerializer(relateds, many=True)  # transforma em json a lista de filmes

        # Gerar gráfico de avaliações dos filmes recomendados
        img_data = ploting.plot_film_ratings(relateds)  # gera o gráfico

        # Preparar a resposta
        data = {"films": serializer.data, "img_data": img_data}

        # Retornar resposta com os dados serializados
        return Response(data, status=status.HTTP_200_OK)

        # ------------------------------ transformando em json eu mesmo ------------------------
        # data = {
        #     "films": [{"id": film.id, "name": film.name, "description": film.description, "rating": film.rating} for
        #               film in relateds],
        #     "img_data": img_data,
        # }
        # return Response(data, status=status.HTTP_200_OK)


class elementosEmComumViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Ao receber uma lista de descrições de filmes em formato json retorna o que eles tem em "
                              "comum",
        manual_parameters=[
            openapi.Parameter(
                name="films",
                in_=openapi.IN_QUERY,  # Especifica que o parâmetro está no corpo da requisição
                description="Lista de descrições dos filmes em formato JSON.",
                required=True,
                type=openapi.TYPE_STRING,
                default="""
                {"films": 
                [
                    {"description": "The epic saga continues as Luke Skywalker learns the ways of the Jedi from Yoda while Darth Vader pursues him."},
                    {"description": "Luke Skywalker and Han Solo team up to rescue Princess Leia and restore peace to the Empire."},
                    {"description": "Luke rescues Han Solo and Leia from Jabba the Hutt, then faces Darth Vader to become a Jedi."},
                    {"description": "Anakin Skywalker turns to the dark side, becoming Darth Vader, while the Jedi are almost destroyed."},
                    {"description": "A space hero and his sidekick fight Dark Helmet to save Princess Vespa and her planet's air supply."}
                ]
                }
                """
            ),
        ],

        responses={200: openapi.Response('Resposta de sucesso'),
                   400: openapi.Response('O parâmetro "films" é obrigatório'),
                   406: openapi.Response('O parâmetro "films" deve estar no formato json'),
                   }
    )

    def analise(self, request):
        films = request.GET.get('films', None)
        if not films:
            return Response({"error": "O parâmetro 'films' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_films = urllib.parse.unquote(films)
        decoded_films = decoded_films.replace("'%27%27%27", "").replace("%27", "'").replace("%22", '"')

        if not analise.is_valid_json(decoded_films):
            return Response({"error": "O parâmetro 'films' deve ser no formato json"}, status=status.HTTP_406_NOT_ACCEPTABLE_BAD_REQUEST)

        result = analise.analise_description(films)
        data = {"semelhancas": result}
        return Response(data, status=status.HTTP_200_OK)
