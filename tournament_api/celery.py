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

tournament_dlx = Exchange("tournament.dlx", type="fanout", durable=True)



app.conf.task_queues = (
    Queue("celery"),
    Queue(
        "tournament-events",
        exchange=tournament_exchange,
        routing_key="tournament.#",
        durable=True,
        queue_arguments={
            "x-dead-letter-exchange": "tournament.dlx",
            "x-message-ttl": 60000 * 10,  # 10 minutes
        },
    ),
    Queue(
        "tournament-events.dlq",
        exchange=tournament_dlx,
        routing_key="",
        durable=True
    )
)

app.conf.task_routes = {
    "eliminationtournaments.tasks.score_request": {"queue": "tournament-events"},
    "eliminationtournaments.tasks.end_match": {"queue": "tournament-events"},
    "eliminationtournaments.tasks.start_tournament": {"queue": "tournament-events"},

    "eliminationtournaments.consumers.ws_fanout": { "queue": "tournament-events" },
}