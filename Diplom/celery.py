import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Diplom.settings')

app = Celery('Diplom')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_currencies_every_three_minutes': {
        'task': 'main.tasks.update_currencies',
        'schedule': crontab()
    }
}
