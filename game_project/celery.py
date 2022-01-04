from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from game_project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_project.settings')
app = Celery('game_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update_db': {
        'task': 'update_db',
        'schedule': crontab(minute=0, hour=0),
    },
}
