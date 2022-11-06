import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('django_coins')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'coins_collect_every_minutes': {
        'task': 'apps.coins.tasks.coins_collect',
        'schedule': crontab(),
    },
}
