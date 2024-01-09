"""
WSGI config for omori project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
import boto3
from omori import settings
from pathlib import Path

load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omori.settings')

application = get_wsgi_application()

bucket_name = "omori-photos"
folder_names = ["alina" , "ivan"]
s3 = boto3.client('s3')
paginator = s3.get_paginator('list_objects_v2')

for folder_name in folder_names:
    local_directory = Path(settings.MEDIA_ROOT) / folder_name
    local_directory.mkdir(parents=True, exist_ok=True)
    for result in paginator.paginate(Bucket=bucket_name, Prefix=folder_name):
            for obj in result['Contents']:
                key = obj['Key']
                if key.endswith('/'):
                    continue
                if not os.path.exists(os.path.dirname(str(local_directory) + key)):
                    os.makedirs(os.path.dirname(str(local_directory) + key))
                s3.download_file(bucket_name, key, str(local_directory) + key)