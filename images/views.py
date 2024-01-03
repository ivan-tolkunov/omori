import os
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.files.storage import default_storage
from pathlib import Path
from datetime import datetime
from django.templatetags.static import static
from django.contrib import messages


from omori import settings

def index(request):
    user = request.GET.get("user")
    if not user:
        return HttpResponse("User not found", status=404)
    
    folder = Path(settings.MEDIA_ROOT) / user
    files = sorted(os.listdir(folder), reverse=True)

    return render(request, "images/index.html", {
        "files": files,
        "latest_file": user + "/" + files[0] if files else None,
        "user": user
    })

def upload_img(request):
    try:
        file = request.FILES.get("image")
        receiver = request.POST.get("receiver")
        user = request.POST.get("user")
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H_%M_%S")
        _, file_extension = os.path.splitext(file.name)
        if file_extension.lower() not in [".png", ".jpeg", ".heic", ".jpg", ".gif"]:
            raise ValueError("Unsupported file extension")
        file_name = Path(settings.MEDIA_ROOT) / receiver / (timestamp + file_extension)
        default_storage.save(file_name, file)
    except:
        messages.add_message(request, messages.ERROR, "Upload failed")
    finally:
        base_url = reverse("index")
        query_string = urlencode({"user": user})
        url = "{}?{}".format(base_url, query_string)
        return redirect(url)

def get_img(request):
    user = request.GET.get("user")
    folder = Path(settings.MEDIA_ROOT) / user
    files = sorted(os.listdir(folder), reverse=True)
    if len(files) < 1:
        image_url = static("img/love-you.gif")
        return redirect(image_url)
    return redirect(settings.MEDIA_URL + user + "/" + files[0])