from kombu import Exchange, Producer
from tournament_api.celery import app
from eliminationtournaments.events.idempotency import is_event_processed, mark_event_processed
tournament_exchange = Exchange(
    name="tournament.events",
    type="topic",
    durable=True,
)


def publish_event(routing_key: str, payload: dict):

    with app.connection_or_acquire() as conn:
        producer = Producer(conn)
        producer.publish(
            payload,
            exchange=tournament_exchange,
            routing_key=routing_key,
            serializer="json",
            declare=[tournament_exchange],
            retry=True,
        )
    