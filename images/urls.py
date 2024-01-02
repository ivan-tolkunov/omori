from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_img, name="upload"),
    path("get-img", views.get_img, name="get_img"),
]