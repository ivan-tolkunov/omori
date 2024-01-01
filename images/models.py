from django import forms
from django.db import models

from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget


class Image(models.Model):
    photo = ImageField(blank=True, manual_crop="")