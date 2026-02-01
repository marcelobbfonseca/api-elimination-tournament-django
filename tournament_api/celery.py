import os
from celery import Celery
from kombu import Exchange, Queue



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tournament_api.settings')

app = Celery('tournament_api')

#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


tournament_exchange = Exchange("tournament.events", type="topic", durable=True)
app.conf.task_queues = (
    Queue(
        "tournament-events",
        exchange=tournament_exchange,
        routing_key="tournament.#",
    ),
)

app.conf.task_routes = {
    "eliminationtournaments.consumers.ws_fanout": {
        "queue": "tournament-events",
    },
}