from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_img, name="upload"),
    path("get-img", views.get_img, name="get_img"),
    path("react", views.add_reaction, name="react"),
    path("get-reactions", views.get_reactions, name="get_reactions"),
]