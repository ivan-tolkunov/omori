import os
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.files.storage import default_storage
from pathlib import Path
from datetime import datetime
from django.templatetags.static import static
from django.contrib import messages
from django.db import IntegrityError
from .models import Image
from django.core.exceptions import ObjectDoesNotExist


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
        if not file:
            raise ValueError("No file uploaded")
        receiver = request.POST.get("receiver")
        user = request.POST.get("user")
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H_%M_%S")
        _, file_extension = os.path.splitext(file.name)
        if file_extension.lower() not in [".png", ".jpeg", ".heic", ".jpg", ".gif"]:
            raise ValueError("Unsupported file extension")
        file_name = Path(settings.MEDIA_ROOT) / receiver / (timestamp + file_extension)
        file_amount_pre = file_amount(receiver)
        default_storage.save(file_name, file)
        if file_amount_pre >= file_amount(receiver):
            raise ValueError("Upload failed")
        messages.add_message(request, messages.INFO, "Upload successful")
    except ValueError as e:
        messages.add_message(request, messages.ERROR, str(e))
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

def add_reaction(request):
    try:
        user = request.POST.get("user")
        reaction = request.POST.get("reaction")
        receiver = request.POST.get("receiver")
        new_reaction = Image(emodji=reaction, receiver=receiver)
        new_reaction.save()
        messages.add_message(request, messages.INFO, "Reaction added")
    except:
        messages.add_message(request, messages.ERROR, "Can't add reaction")
    finally:
        base_url = reverse("index")
        query_string = urlencode({"user": user})
        url = "{}?{}".format(base_url, query_string)
        return redirect(url)
    

def get_reactions(request):
    user = request.GET.get("user")
    if not user:
        return HttpResponseBadRequest("User parameter is required")
    try:
        reactions = Image.objects.filter(receiver=user).values('emodji')
        response_body = [reaction['emodji'] for reaction in reactions]
        Image.objects.filter(receiver=user).delete()
    except:
        return HttpResponseBadRequest("No reactions found for the given user")
    finally:
        return JsonResponse(response_body, safe=False)
    
def file_amount(user):
    return len(os.listdir( Path(settings.MEDIA_ROOT) / user))