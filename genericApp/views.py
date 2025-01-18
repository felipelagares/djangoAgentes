from django.shortcuts import render, get_object_or_404, redirect
from .models import File


def file_upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # Obtém o arquivo enviado no formulário
        uploaded_name = request.FILES.get('name')
        if not uploaded_name:
            uploaded_name = uploaded_file.name

        if uploaded_file:
            File.objects.create(name=uploaded_name, file=uploaded_file)
            return redirect('file_list')
    return render(request, 'file_upload.html')


def file_update_view(request, pk):
    file_instance = get_object_or_404(File, pk=pk)  # Obtém o registro

    if 'action' in request.POST and request.POST['action'] == 'delete':
        file_instance.delete()
        return redirect('file_list')

    if request.method == 'POST':
        file_instance['name'] = request['name']
        file_instance['file'] = request['file']
        file_instance.save()
        return redirect('file_list')

    return render(request, 'file_update.html', {'file': file_instance})


def file_list_view(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})
