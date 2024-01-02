from django import forms
from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    