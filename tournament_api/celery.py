import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tournament_api.settings')

app = Celery('tournament_api',
             broker='amqp://admin:admin@rabbitmq:5672//',
             backend='rpc://',
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()