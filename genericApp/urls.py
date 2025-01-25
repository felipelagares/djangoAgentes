from django.urls import path
from . import views


# urls de acesso, referenciados no html por 'name' e ligados a cada respectiva view que processa a requisição
urlpatterns = [
    path('', views.file_list_view, name='file_list'),  # Página inicial que lista os arquivos
    path('upload/', views.file_upload_view, name='file_upload'),  # Página para upload de arquivos
    path('file/update/<int:pk>/', views.file_update_view, name='file_update'),  # Página para visualização de arquivos
    path('recomendation/', views.related_films_view, name='related_films'),  # Página para recomendaçao de filmes
    path('film/<int:pk>/', views.film_details_view, name='film_details'),  # Página para visualização de filmes
]
