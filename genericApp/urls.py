from django.urls import path
from . import views
from .views import RecommendationViewSet, elementosEmComumViewSet

# Criar o endpoint de recomendação
recommendation_list = RecommendationViewSet.as_view({'get': 'recommend'})
analise = elementosEmComumViewSet.as_view({'get': 'analise'})

# URLs de acesso
urlpatterns = [
    path('', views.file_list_view, name='file_list'),  # Página inicial que lista os arquivos
    path('upload/', views.file_upload_view, name='file_upload'),  # Página para upload de arquivos
    path('file/update/<int:pk>/', views.file_update_view, name='file_update'),  # Página para visualização de arquivos
    path('recomendation/', views.related_films_view, name='related_films'),  # Página para recomendações de filmes
    path('film/<int:pk>/', views.film_details_view, name='film_details'),  # Página para visualização de filmes

    # Endpoint de recomendação na API
    path('api/recommendations/', recommendation_list, name='film_recommendation'),
    path('api/analise', analise, name='films_analise' )# API para recomendações de filmes
]
