# newsaggregator/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsaggregator.settings')

app = Celery('newsaggregator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
