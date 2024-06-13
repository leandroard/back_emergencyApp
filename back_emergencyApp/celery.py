from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

environment = os.environ.get('ENVIRONMENT', 'development')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back_emergencyApp.settings.{}".format(environment))

app = Celery('back_emergencyApp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



app.conf.beat_schedule = {
    'update-emergency-status-every-minute': {
        'task': 'emergencies.tasks.update_emergency_status',
        'schedule': crontab(minute='*'),  # Ejecuta cada minuto
    },
}
