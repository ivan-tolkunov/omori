import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pyuploadcare import Uploadcare, File
from django.core.files.storage import default_storage
from pathlib import Path

from omori import settings

def index(request):
    return render(request, "images/index.html")

def get_img(request):
    file = request.FILES.get('image')
    file_name = Path(settings.MEDIA_ROOT) / Path(default_storage.save(file.name, file))
    upload(file_name)
    default_storage.delete(file_name)
    return redirect('index')

def upload(file_name):
    uploadcare = Uploadcare(public_key='f46fb1fa74d411e2ca9a', secret_key='2e28fcf62e0258d170de')
    with open(file_name, 'rb') as file_object:
        uc_file: File = uploadcare.upload(file_object, store=True)
        print(uc_file.info)