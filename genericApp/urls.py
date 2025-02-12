from django.urls import path, re_path
from . import views
from .views import RecommendationViewSet, elementosEmComumViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API do recomendador de filmes",
        default_version='v1',
        description="Documentação da API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
    path('api/analise', analise, name='films_analise'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
