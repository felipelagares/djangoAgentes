from django.shortcuts import render, get_object_or_404, redirect
from .models import File, Film
from .src import recomendation
from .src import ploting


def file_upload_view(request):
    # view para receber um arquivo
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        uploaded_name = request.POST.get('name')
        if not uploaded_name:
            uploaded_name = uploaded_file.name

        if uploaded_file:
            File.objects.create(name=uploaded_name, file=uploaded_file)
            return redirect('file_list')
    return render(request, 'file_upload.html')


def file_update_view(request, pk):
    # view para atualizar/deletar um arquivo
    file_instance = get_object_or_404(File, pk=pk)  # Obtém o registro

    if 'action' in request.POST and request.POST['action'] == 'delete':
        file_instance.delete()
        return redirect('file_list')

    if request.method == 'POST':
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
