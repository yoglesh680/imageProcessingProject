from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import signals

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_processor.settings')

app = Celery('image_processor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@signals.setup_logging.connect
def setup_logging(**kwargs):
    pass
