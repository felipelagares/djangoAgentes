from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list_view, name='file_list'),  # Página inicial que lista os arquivos
    path('upload/', views.file_upload_view, name='file_upload'),  # Página para upload de arquivos
    path('file/update/<int:pk>/', views.file_update_view, name='file_update'),
]
