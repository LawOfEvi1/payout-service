# src/config/celery.py
import os
from celery import Celery

# Используем переменную окружения для Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('payout_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # автоматически находит tasks.py в apps