from django import forms
from django.db import models

class Image(models.Model):
    emodji = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    
    