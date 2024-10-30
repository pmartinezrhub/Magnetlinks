# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configura la aplicación Django para que Celery pueda acceder a ella
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magnetlinks.settings')
app = Celery('magnetlinks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
