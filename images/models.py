from django import forms
from django.db import models

from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget


class Image(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    