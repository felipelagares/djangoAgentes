from django.shortcuts import render, redirect
from .models import File


def file_upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # Obtém o arquivo enviado no formulário
        if uploaded_file:
            File.objects.create(file=uploaded_file)  # Cria uma nova instância do modelo File
            return redirect('file_list')  # Redireciona para a lista de arquivos
    return render(request, 'file_upload.html')


def file_list_view(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})
