"""
WSGI config for omori project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from omori import settings
from pathlib import Path

load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omori.settings')

application = get_wsgi_application()

folder_names = ["alina" , "ivan"]
for folder_name in folder_names:
    local_directory = Path(settings.MEDIA_ROOT) / folder_name
    local_directory.mkdir(parents=True, exist_ok=True)
   